from src.df import CreateJobDataFrame, save_df_to_csv
from src.get_input import GetUserInput
from src.pipeline import JobDataPipeline

def collect_data():
    user_input = GetUserInput.run_get_input()

    pipeline = JobDataPipeline()
    pipeline.run(job_title=user_input.job_title, location=user_input.location,
     search_radius=user_input.search_radius, max_pages=user_input.max_pages,
     get_full_descriptions=user_input.get_description)

    df = CreateJobDataFrame.create_df(pipeline.formatted_results)

    save_df_to_csv(df, user_input.save_name)