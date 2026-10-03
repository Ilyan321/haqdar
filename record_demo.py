import asyncio
import os
import shutil
import glob
from playwright.async_api import async_playwright

VIDEO_DIR = "/home/ilyan/og/.gsd/video_recordings"
FINAL_OUTPUT = "/home/ilyan/Videos/Screencasts/haqdar_perfect_demo.mp4"

async def human_type(page, selector, text, delay=30):
    """Types text like a human into the selector."""
    await page.click(selector, force=True)
    await page.wait_for_timeout(300)
    for char in text:
        await page.type(selector, char, delay=delay)
    await page.wait_for_timeout(500)

async def record():
    os.makedirs(VIDEO_DIR, exist_ok=True)
    for f in glob.glob(f"{VIDEO_DIR}/*"):
        try:
            os.remove(f)
        except Exception:
            pass

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
            device_scale_factor=1,
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        print("[1/9] Navigating to HaqDar dashboard...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # 1. Start with natural Roman Urdu intake
        print("[2/9] Typing opening case statement...")
        input_selector = "textarea"
        await human_type(
            page, 
            input_selector, 
            "Mera walid marhoom ho gaye hain aur mere bhaiyon ne Lahore ki saari zameen apne naam karwa li hai aur mujhe hissa nahi de rahe.",
            delay=25
        )
        
        # Click send button
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        print("[3/9] Waiting for Intake Agent response (Question 1)...")
        await page.wait_for_timeout(4500)

        # 2. Answer with deceased name and date of death
        print("[4/9] Typing deceased details...")
        await human_type(
            page,
            input_selector,
            "Walid ka naam Chaudhry Muhammad Din tha, inteqal 14 March 2023 ko hua",
            delay=25
        )
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        print("[5/9] Waiting for Intake Agent response (Question 2)...")
        await page.wait_for_timeout(4500)

        # 3. Answer with family heirs breakdown
        print("[6/9] Typing heir roster...")
        await human_type(
            page,
            input_selector,
            "2 betay (Tariq aur Rashid), 1 beti (Fatima - main), aur walida (widow Kulsoom) hayat hain",
            delay=25
        )
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        print("[7/9] Waiting for Intake Agent response (Question 3)...")
        await page.wait_for_timeout(4500)

        # 4. Answer with property size and location
        print("[8/9] Typing property measurement...")
        await human_type(
            page,
            input_selector,
            "16 Kanal agricultural zameen hai Raiwind Lahore mein",
            delay=25
        )
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(5000)

        # 5. Launch the 8-Agent Autonomous Investigation
        print("[9/9] Launching 8-Agent Investigation...")
        launch_btn = page.locator("button:has-text('Launch 8-Agent Autonomous Investigation'), button:has-text('All Facts Complete')")
        if await launch_btn.count() > 0:
            await launch_btn.first.click(force=True)
        else:
            quick_launch = page.locator("button:has-text('8-Agent Investigation')")
            if await quick_launch.count() > 0:
                await quick_launch.first.click(force=True)

        print("Investigation running. Observing live Agent Topology...")
        for sec in range(1, 40):
            await page.wait_for_timeout(1000)
            completed_badge = page.locator("text=100% QA Validated, text=Judicial Grade Dossier")
            if await completed_badge.count() > 0 and sec > 15:
                print(f"Investigation completed at second {sec}!")
                break

        await page.wait_for_timeout(4000)

        # Tour all the tabs smoothly
        print("Showcasing Tab 1: Agent Topology...")
        topology_tab = page.locator("button:has-text('Agent Topology')")
        if await topology_tab.count() > 0:
            await topology_tab.first.click(force=True)
            await page.wait_for_timeout(4000)

        print("Showcasing Tab 2: Shajra Nasab (Family Tree Graph)...")
        shajra_tab = page.locator("button:has-text('Shajra Nasab')")
        if await shajra_tab.count() > 0:
            await shajra_tab.first.click(force=True)
            await page.wait_for_timeout(4500)

        print("Showcasing Tab 3: Deed Forensic (Fraud Analysis)...")
        deed_tab = page.locator("button:has-text('Deed Forensic')")
        if await deed_tab.count() > 0:
            await deed_tab.first.click(force=True)
            await page.wait_for_timeout(4500)

        print("Showcasing Tab 4: QA Reflection (Mathematical Closure)...")
        qa_tab = page.locator("button:has-text('QA Reflection')")
        if await qa_tab.count() > 0:
            await qa_tab.first.click(force=True)
            await page.wait_for_timeout(4000)

        # Scroll down to showcase Share Matrix & Legal Dossier
        print("Scrolling down to Share Breakdown & Legal Dossier...")
        await page.evaluate("window.scrollBy({ top: 450, behavior: 'smooth' })")
        await page.wait_for_timeout(4000)

        # Toggle Roman Urdu Dossier
        print("Toggling Roman Urdu dossier view...")
        urdu_toggle = page.locator("button:has-text('Roman Urdu')")
        if await urdu_toggle.count() > 0:
            await urdu_toggle.first.click(force=True)
            await page.wait_for_timeout(3500)

        # Toggle back to English
        print("Toggling English dossier view...")
        eng_toggle = page.locator("button:has-text('English')")
        if await eng_toggle.count() > 0:
            await eng_toggle.first.click(force=True)
            await page.wait_for_timeout(3500)

        # Scroll back to top for final clean summary view
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await page.wait_for_timeout(4000)

        print("Recording finished successfully!")
        await page.close()
        await context.close()
        await browser.close()

    # Find the recorded video file and convert to high quality MP4
    video_files = glob.glob(f"{VIDEO_DIR}/*.webm") + glob.glob(f"{VIDEO_DIR}/*.mp4")
    if video_files:
        raw_video = video_files[0]
        os.makedirs(os.path.dirname(FINAL_OUTPUT), exist_ok=True)
        print(f"Raw video saved at: {raw_video}")
        cmd = f'ffmpeg -y -i "{raw_video}" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p "{FINAL_OUTPUT}"'
        os.system(cmd)
        print(f"Final polished MP4 created at: {FINAL_OUTPUT}")
    else:
        print("No video file found!")

if __name__ == "__main__":
    asyncio.run(record())
