import asyncio
import os
import glob
from playwright.async_api import async_playwright

VIDEO_DIR = "/home/ilyan/og/.gsd/fast_video_recordings"
RAW_OUTPUT = "/home/ilyan/og/.gsd/fast_raw.mp4"
FINAL_OUTPUT = "/home/ilyan/Videos/Screencasts/haqdar_fast_demo.mp4"

async def fast_human_type(page, selector, text, delay=14):
    """Types text smoothly and rapidly into the selector."""
    await page.click(selector, force=True)
    await page.wait_for_timeout(150)
    for char in text:
        await page.type(selector, char, delay=delay)
    await page.wait_for_timeout(250)

async def record_fast():
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

        print("[1/8] Navigating to HaqDar dashboard...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(1800)

        # 1. Opening message
        input_selector = "textarea"
        print("[2/8] Conversational discovery (Opening)...")
        await fast_human_type(
            page, 
            input_selector, 
            "Mera walid marhoom ho gaye hain aur mere bhaiyon ne Lahore ki saari zameen apne naam karwa li hai aur mujhe hissa nahi de rahe.",
            delay=12
        )
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(3200)

        # 2. Deceased details
        print("[3/8] Answering deceased name...")
        await fast_human_type(
            page,
            input_selector,
            "Walid ka naam Chaudhry Muhammad Din tha, inteqal 14 March 2023 ko hua",
            delay=12
        )
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(3200)

        # 3. Family heirs
        print("[4/8] Answering heirs roster...")
        await fast_human_type(
            page,
            input_selector,
            "2 betay (Tariq aur Rashid), 1 beti (Fatima - main), aur walida (widow Kulsoom) hayat hain",
            delay=12
        )
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(3200)

        # 4. Property details
        print("[5/8] Answering property size...")
        await fast_human_type(
            page,
            input_selector,
            "16 Kanal agricultural zameen hai Raiwind Lahore mein",
            delay=12
        )
        await page.click("button:has(svg.lucide-send), form button[type='submit']", force=True)
        await page.wait_for_timeout(3500)

        # 5. Launch Swarm
        print("[6/8] Launching 8-Agent Autonomous Swarm...")
        launch_btn = page.locator("button:has-text('Launch 8-Agent Autonomous Investigation'), button:has-text('All Facts Complete')")
        if await launch_btn.count() > 0:
            await launch_btn.first.click(force=True)
        else:
            quick_launch = page.locator("button:has-text('8-Agent Investigation')")
            if await quick_launch.count() > 0:
                await quick_launch.first.click(force=True)

        print("Swarm executing live. Actively guiding visual focus...")
        # Smoothly move mouse across the active nodes as they process to keep visual interest
        nodes = [
            "text=Intake Agent",
            "text=Case Orchestrator",
            "text=Family Tree",
            "text=Document Analyzer",
            "text=Sharia Calculator",
            "text=Fraud Detection",
            "text=Legal Strategy",
            "text=QA Reviewer"
        ]
        
        start_time = asyncio.get_event_loop().time()
        node_idx = 0
        while asyncio.get_event_loop().time() - start_time < 35:
            # Hover current node
            target = page.locator(nodes[node_idx % len(nodes)])
            if await target.count() > 0:
                try:
                    await target.first.hover(timeout=1000)
                except Exception:
                    pass
            node_idx += 1
            await page.wait_for_timeout(1800)
            
            # Check if investigation completed
            completed_badge = page.locator("text=100% QA Validated, text=Judicial Grade Dossier")
            if await completed_badge.count() > 0 and (asyncio.get_event_loop().time() - start_time) > 12:
                print("Investigation finished!")
                break

        await page.wait_for_timeout(2000)

        # 6. Smooth rapid tour of all tabs
        print("[7/8] Showcasing all tabs rapidly...")
        
        # Tab 1: Agent Topology
        topology_tab = page.locator("button:has-text('Agent Topology')")
        if await topology_tab.count() > 0:
            await topology_tab.first.click(force=True)
            await page.wait_for_timeout(2200)

        # Tab 2: Shajra Nasab
        shajra_tab = page.locator("button:has-text('Shajra Nasab')")
        if await shajra_tab.count() > 0:
            await shajra_tab.first.click(force=True)
            await page.wait_for_timeout(2800)

        # Tab 3: Deed Forensic
        deed_tab = page.locator("button:has-text('Deed Forensic')")
        if await deed_tab.count() > 0:
            await deed_tab.first.click(force=True)
            await page.wait_for_timeout(2800)

        # Tab 4: QA Reflection
        qa_tab = page.locator("button:has-text('QA Reflection')")
        if await qa_tab.count() > 0:
            await qa_tab.first.click(force=True)
            await page.wait_for_timeout(2500)

        # 7. Scroll down to show Faraizi Table & Judicial Dossier
        print("[8/8] Showcasing Share Table and Bilingual Legal Dossier...")
        await page.evaluate("window.scrollBy({ top: 460, behavior: 'smooth' })")
        await page.wait_for_timeout(2500)

        # Toggle Roman Urdu
        urdu_toggle = page.locator("button:has-text('Roman Urdu')")
        if await urdu_toggle.count() > 0:
            await urdu_toggle.first.click(force=True)
            await page.wait_for_timeout(2200)

        # Toggle back to English
        eng_toggle = page.locator("button:has-text('English')")
        if await eng_toggle.count() > 0:
            await eng_toggle.first.click(force=True)
            await page.wait_for_timeout(2200)

        # Scroll back to top for clean finale
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await page.wait_for_timeout(2500)

        print("Fast demo recording complete!")
        await page.close()
        await context.close()
        await browser.close()

    # Convert with ffmpeg
    video_files = glob.glob(f"{VIDEO_DIR}/*.webm") + glob.glob(f"{VIDEO_DIR}/*.mp4")
    if video_files:
        raw_video = video_files[0]
        os.makedirs(os.path.dirname(FINAL_OUTPUT), exist_ok=True)
        cmd = f'ffmpeg -y -i "{raw_video}" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p "{FINAL_OUTPUT}"'
        os.system(cmd)
        print(f"Option B (Fast Action Cut) saved at: {FINAL_OUTPUT}")

if __name__ == "__main__":
    asyncio.run(record_fast())
