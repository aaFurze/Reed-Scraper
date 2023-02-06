from src.df import CreateJobDataFrame, save_df_to_csv
from src.get_input import GetUserInput
from src.pipeline import DetailedJobDataPipeline, JobDataPipeline


def run():
    user_input = GetUserInput.run_get_input()

    pipeline = JobDataPipeline()
    pipeline.run(job_title= user_input.job_title, location=user_input.location,
     search_radius=user_input.search_radius, max_pages=user_input.max_pages)

    df = CreateJobDataFrame.create_blank_df(detailed_columns=user_input.get_description)

    if user_input.get_description:
        detailed_pipeline = DetailedJobDataPipeline()
        detailed_pipeline.run([result.job_id for result in pipeline.formatted_results])

        CreateJobDataFrame.insert_mutliple_detailed_job_information_objects_into_df(df, 
            pipeline.formatted_results, detailed_job_infos=detailed_pipeline.formatted_results)
    else:
        CreateJobDataFrame.insert_mutliple_job_information_objects_into_df(df, pipeline.formatted_results)

    save_df_to_csv(df, user_input.save_name)


if __name__ == "__main__":
    run()
    