import asyncio
import logging
import os
from typing import Any, Dict, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger("haqdar.notifier")

class SlackNotifier:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    @property
    def webhook_url(self) -> str:
        return (
            os.getenv("SLACK_WEBHOOK_URL")
            or getattr(settings, "SLACK_WEBHOOK_URL", "")
            or os.getenv("ALERT_WEBHOOK_URL")
            or getattr(settings, "ALERT_WEBHOOK_URL", "")
        )

    @property
    def bot_token(self) -> str:
        return (
            os.getenv("SLACK_BOT_TOKEN")
            or getattr(settings, "SLACK_BOT_TOKEN", "")
        )

    @property
    def channel_id(self) -> str:
        return (
            os.getenv("SLACK_CHANNEL_ID")
            or getattr(settings, "SLACK_CHANNEL_ID", "")
            or "C0BGMV9SS1K"  # default to agy channel
        )

    def build_slack_blocks(self, session_id: str, dossier: Dict[str, Any]) -> Dict[str, Any]:
        intake = dossier.get("intake", {})
        classification = dossier.get("classification", {})
        sharia = dossier.get("sharia_distribution", {})
        fraud = dossier.get("fraud_report", {})
        roadmap = dossier.get("legal_roadmap", {})
        bilingual = dossier.get("bilingual_report", {})

        deceased_name = intake.get("deceased_name", "Unknown Deceased")
        province = classification.get("province", "Federal / Pakistan")
        forum = roadmap.get("priority_forum", "Ombudsperson Forum")
        fraud_alerts = fraud.get("alerts", [])
        critical_count = fraud.get("critical_alerts_count", len(fraud_alerts))

        # Build properties summary
        props = intake.get("properties", [])
        prop_str = ", ".join([f"{p.get('area_description', '')} in {p.get('location', '')}" for p in props]) if props else "Disputed Real Estate"

        # Build heirs summary
        allocations = sharia.get("heir_allocations", [])
        heir_lines = []
        for h in allocations:
            claimant_badge = " *(Claimant)*" if h.get("relationship") in ["daughter", "wife", "sister"] else ""
            heir_lines.append(
                f"• *{h.get('name', 'Heir')}* ({h.get('relationship', 'Relation')}): `{h.get('exact_fraction_str', '')}` ({h.get('share_percentage', 0):.2f}%) — {h.get('allocated_area', '')}{claimant_badge}"
            )
        heirs_formatted = "\n".join(heir_lines) if heir_lines else "Lawful heirs calculated according to Quran 4:11 & 4:12"

        # Fraud summary
        fraud_summary_list = []
        for alert in fraud_alerts[:2]:
            fraud_summary_list.append(f"• 🚨 *{alert.get('fraud_type', 'Violation')}*: {alert.get('deprivation_summary', '')}")
        fraud_formatted = "\n".join(fraud_summary_list) if fraud_summary_list else "Potential unlawful dispossession under PPC 498A"

        case_url = "https://haqdar.aenox.me"

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "⚖️ HaqDar: New Inheritance Investigation Completed",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Case ID:*\n`{session_id}`"},
                    {"type": "mrkdwn", "text": f"*Deceased / Estate:*\n{deceased_name}"},
                    {"type": "mrkdwn", "text": f"*Jurisdiction:*\n{province}"},
                    {"type": "mrkdwn", "text": f"*Fast-Track Forum:*\n{forum}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🏡 Disputed Property / Estate:*\n{prop_str}"
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*📜 Deterministic Quranic Shares (Quran 4:11-12):*\n{heirs_formatted}"
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🚨 Forensic Deprivation Audit ({critical_count} Alert{'s' if critical_count != 1 else ''}):*\n{fraud_formatted}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🏛️ Fast-Track Legal Strategy:*\n{roadmap.get('primary_strategy', 'Ombudsperson Section 4 Restoration Petition')} *(Statutory Limit: 60 Days)*"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "View Live Case on HaqDar",
                            "emoji": True
                        },
                        "url": case_url,
                        "style": "primary"
                    }
                ]
            }
        ]

        return {
            "text": f"⚖️ HaqDar: Case {session_id} Investigation Complete for {deceased_name}'s estate ({prop_str})",
            "blocks": blocks
        }

    async def send_investigation_alert(self, session_id: str, dossier: Dict[str, Any]) -> bool:
        payload = self.build_slack_blocks(session_id, dossier)

        # 1. Prefer Bot Token API if configured
        if self.bot_token:
            try:
                post_data = {
                    "channel": self.channel_id,
                    "text": payload["text"],
                    "blocks": payload["blocks"]
                }
                headers = {
                    "Authorization": f"Bearer {self.bot_token}",
                    "Content-Type": "application/json; charset=utf-8"
                }
                response = await self.client.post("https://slack.com/api/chat.postMessage", json=post_data, headers=headers)
                data = response.json()
                if data.get("ok"):
                    logger.info("SlackNotifier: Alert sent via Bot API for session %s", session_id)
                    return True
                else:
                    logger.warning("SlackNotifier: Bot API error: %s", data.get("error"))
            except Exception as e:
                logger.error("SlackNotifier: Bot API exception: %s", str(e))

        # 2. Fallback to Webhook URL
        if self.webhook_url:
            try:
                response = await self.client.post(self.webhook_url, json=payload)
                if response.status_code in [200, 204]:
                    logger.info("SlackNotifier: Alert sent via Webhook for session %s", session_id)
                    return True
                else:
                    logger.warning("SlackNotifier: Webhook post failed (%s): %s", response.status_code, response.text)
                    return False
            except Exception as e:
                logger.error("SlackNotifier: Webhook exception: %s", str(e))
                return False

        logger.info("SlackNotifier: Neither Bot Token nor Webhook URL configured.")
        return False

    def trigger_async_alert(self, session_id: str, dossier: Dict[str, Any]) -> None:
        """Fire and forget without blocking the response."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.send_investigation_alert(session_id, dossier))
        except RuntimeError:
            asyncio.run(self.send_investigation_alert(session_id, dossier))

notifier = SlackNotifier()
