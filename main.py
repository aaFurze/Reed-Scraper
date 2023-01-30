from src.df import CreateJobDataFrame, save_df_to_csv
from src.pipeline import DetailedJobDataPipeline, JobDataPipeline

if __name__ == "__main__":
    pipeline = JobDataPipeline()
    pipeline.run(job_title="Software Engineer", location="Leeds ", search_radius=10,
     max_pages=3)

    detailed_pipeline = DetailedJobDataPipeline()
    detailed_pipeline.run([result.job_id for result in pipeline.formatted_results])

    df = CreateJobDataFrame.create_blank_df(detailed_columns=True)
    CreateJobDataFrame.insert_mutliple_detailed_job_information_objects_into_df(df, 
        pipeline.formatted_results, detailed_job_infos=detailed_pipeline.formatted_results)
    save_df_to_csv(df, "test_software_engineer_leeds_10_miles")
    