import asyncio
import os
import sys
from pathlib import Path

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.notifier import notifier

async def main():
    bot_token = notifier.bot_token
    webhook_url = notifier.webhook_url
    if not bot_token and not webhook_url:
        print("⚠️ Neither SLACK_BOT_TOKEN nor SLACK_WEBHOOK_URL is set in environment or .env!")
        return

    if bot_token:
        print(f"📡 Dispatching mock case investigation alert via Bot API (Channel: {notifier.channel_id})...")
    else:
        print(f"📡 Dispatching mock case investigation alert to Webhook: {webhook_url[:35]}...")
    mock_dossier = {
        "intake": {
            "deceased_name": "Chaudhry Muhammad Aslam",
            "properties": [{"area_description": "120 Kanals Agricultural Land", "location": "District Kasur, Punjab"}],
            "family_members": [{"name": "Fatima Aslam", "relationship": "daughter"}]
        },
        "classification": {
            "province": "Punjab",
            "applicable_act": "Punjab Enforcement of Women's Property Rights Act 2021"
        },
        "sharia_distribution": {
            "heir_allocations": [
                {
                    "name": "Fatima Aslam",
                    "relationship": "daughter",
                    "exact_fraction_str": "27/160",
                    "share_percentage": 16.875,
                    "allocated_area": "20.25 Kanals"
                },
                {
                    "name": "Zainab Aslam",
                    "relationship": "daughter",
                    "exact_fraction_str": "27/160",
                    "share_percentage": 16.875,
                    "allocated_area": "20.25 Kanals"
                },
                {
                    "name": "Tariq Aslam",
                    "relationship": "son",
                    "exact_fraction_str": "27/80",
                    "share_percentage": 33.75,
                    "allocated_area": "40.50 Kanals"
                }
            ]
        },
        "fraud_report": {
            "critical_alerts_count": 2,
            "alerts": [
                {
                    "fraud_type": "Omitted Female Heir (PPC 498A)",
                    "deprivation_summary": "Fatima Aslam excluded from Mutation #1042 in Mauza Raja Jang, Kasur."
                }
            ]
        },
        "legal_roadmap": {
            "priority_forum": "Punjab Ombudsperson for Protection of Women's Property Rights",
            "primary_strategy": "Emergency Section 4 Restoration Petition"
        }
    }

    success = await notifier.send_investigation_alert("test-session-498a", mock_dossier)
    if success:
        print("✅ Alert sent successfully! Check your Slack channel.")
    else:
        print("❌ Failed to send alert. Check logs above.")

if __name__ == "__main__":
    asyncio.run(main())
