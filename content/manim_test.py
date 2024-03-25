from manim import *

class AsyncProcessingExplanation(Scene):
    def construct(self):
        # Add title
        title = Text("Asynchronous Processing", color=BLUE, font_size=48)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Add code snippet
        code = Code(
            code="""
import asyncio
import nest_asyncio
import pandas as pd
from signalfloweeg.io import get_amplitude_statistics

async def process_file(filename):
    print(f"Processing file: {filename}")
    result = get_amplitude_statistics(filename, 'EEGLAB_RAW_SET')
    return result

async def process_files(df):
    tasks = []
    for _, row in df.iterrows():
        filename = row['FullFile']
        task = asyncio.create_task(process_file(filename))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    result_df = pd.DataFrame(results)
    return result_df

filelist = pd.read_csv(path.join(analysispath, 'data/01_sprest_filelist.csv'))
df = filelist

nest_asyncio.apply()

presource_df = await process_files(df)
print("Final Result DataFrame:")
print(presource_df)

presource_df.to_csv(path.join(analysispath, 'data/02_sprest_filelist_amplitudes.csv'), index=False)
""",
            language="python",
            font_size=16,
            tab_width=4,
            background="window",
            insert_line_no=False,
            style="monokai",
            background_stroke_width=1,
            background_stroke_color=WHITE,
            corner_radius=0.1,
        )
        code.scale(0.7)
        code.shift(UP * 0.5)

        # Add narration text
        narration_text = [
            "The code demonstrates asynchronous processing using the asyncio library in Python.",
            "The process_file function processes a single file asynchronously.",
            "The process_files function creates tasks for each file and processes them concurrently.",
            "The nest_asyncio library is used to allow asyncio usage in Jupyter Notebook.",
            "The filelist is loaded from a CSV file using pandas.",
            "The process_files function is called with the filelist DataFrame.",
            "The results are stored in a new DataFrame called presource_df.",
            "Finally, the presource_df is saved to a new CSV file.",
        ]

        narration_paragraphs = VGroup()
        for text in narration_text:
            paragraph = Paragraph(text, font_size=20, width=config.frame_width - 1)
            paragraph.next_to(code, DOWN, buff=0.3)
            narration_paragraphs.add(paragraph)

        # Animate the code and narration
        self.play(Create(code))
        for paragraph in narration_paragraphs:
            self.play(Write(paragraph), run_time=2)
            self.wait(1)
            self.play(FadeOut(paragraph))

        # Highlight important parts of the code
        # Highlight important parts of the code
        self.highlight_code(code, "async def process_file(filename):", "process_file function")
        self.highlight_code(code, "async def process_files(df):", "process_files function")
        self.highlight_code(code, "nest_asyncio.apply()", "nest_asyncio usage")
        self.highlight_code(code, "presource_df = await process_files(df)", "Calling process_files")

        self.wait(2)

    def highlight_code(self, code, line, description):
        # Ensure that get_part_by_text is used correctly according to your Manim version
        # This is a generic fix and might need adjustment
        try:
            highlight = code.get_part_by_text(line)
        except TypeError:
            # Adjust this part if Manim's API has changed
            print("Error: Unable to highlight the code. Check the Manim version and method usage.")
            return

        highlight.set_stroke(color=YELLOW, width=2)

        text = Text(description, font_size=24, color=YELLOW)
        text.next_to(code, DOWN, buff=0.5)

        self.play(ShowPassingFlash(highlight.copy().set_color(YELLOW)), Write(text))
        self.wait(2)
        self.play(FadeOut(text))
        
# To run this script, save it as a .py file and execute it with Manim.
# For example, if you save this script as async_flow.py, you can run:
# manim -p -ql async_flow.py AsyncProcessingFlow
