import asyncio
import os
from playwright.async_api import async_playwright

OUTPUT_DIR = "/home/ilyan/og/slides_assets"

async def capture_screenshots():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--font-render-hinting=none"
            ]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2  # Retina 2x for ultra-sharp presentation slides
        )
        page = await context.new_page()

        print("[1/8] Capturing Hero Dashboard...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{OUTPUT_DIR}/01_hero_dashboard.png", full_page=False)

        # 1. Fill in case facts
        print("[2/8] Conversational intake with Roman Urdu...")
        input_selector = "textarea"
        await page.click(input_selector, force=True)
        await page.fill(input_selector, "Mera walid marhoom ho gaye hain aur mere bhaiyon ne Lahore ki saari zameen apne naam karwa li hai aur mujhe hissa nahi de rahe.")
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(3500)

        await page.fill(input_selector, "Walid ka naam Chaudhry Muhammad Din tha, inteqal 14 March 2023 ko hua")
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(3500)

        await page.fill(input_selector, "2 betay (Tariq aur Rashid), 1 beti (Fatima - main), aur walida (widow Kulsoom) hayat hain")
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(3500)

        await page.fill(input_selector, "16 Kanal agricultural zameen hai Raiwind Lahore mein")
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(4000)

        print("[3/8] Capturing Locked Facts & Interactive Intake...")
        await page.screenshot(path=f"{OUTPUT_DIR}/02_conversational_intake_locked_facts.png", full_page=False)

        # Launch Swarm
        print("[4/8] Launching 8-Agent Investigation Swarm...")
        launch_btn = page.locator("button:has-text('Launch 8-Agent Autonomous Investigation'), button:has-text('All Facts Complete')")
        if await launch_btn.count() > 0:
            await launch_btn.first.click(force=True)
        else:
            await page.click("button:has-text('8-Agent Investigation')", force=True)

        for sec in range(1, 40):
            await page.wait_for_timeout(1000)
            completed_badge = page.locator("text=100% QA Validated, text=Judicial Grade Dossier")
            if await completed_badge.count() > 0 and sec > 15:
                print(f"Investigation completed in {sec} seconds!")
                break

        await page.wait_for_timeout(3000)

        # Tab 1: Agent Topology
        print("[5/8] Capturing Agent Topology...")
        await page.click("button:has-text('Agent Topology')", force=True)
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f"{OUTPUT_DIR}/03_agent_topology_completed.png", full_page=False)

        # Tab 2: Shajra Nasab
        print("[6/8] Capturing Shajra Nasab (Family Tree)...")
        await page.click("button:has-text('Shajra Nasab')", force=True)
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f"{OUTPUT_DIR}/04_shajra_nasab_family_tree.png", full_page=False)

        # Tab 3: Deed Forensic
        print("[7/8] Capturing Deed Forensics (Fraud Alert)...")
        await page.click("button:has-text('Deed Forensic')", force=True)
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f"{OUTPUT_DIR}/05_deed_forensic_fraud_alert.png", full_page=False)

        # Tab 4: QA Reflection
        print("[8/8] Capturing QA Reflection...")
        await page.click("button:has-text('QA Reflection')", force=True)
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f"{OUTPUT_DIR}/06_qa_reflection_mathematical_closure.png", full_page=False)

        # Share Table & Dossier
        print("Capturing Share Table & Judicial Dossier...")
        await page.evaluate("window.scrollBy({ top: 480, behavior: 'smooth' })")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{OUTPUT_DIR}/07_deterministic_sharia_table.png", full_page=False)

        # Capture Dossier view
        await page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{OUTPUT_DIR}/08_judicial_dossier_roadmap.png", full_page=False)

        print("All 8 high-definition slide assets captured successfully!")
        await page.close()
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_screenshots())
