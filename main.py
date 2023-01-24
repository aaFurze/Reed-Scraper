from src.df import CreateJobDataFrame, save_df_to_csv
from src.pipeline import JobDataPipeline

if __name__ == "__main__":
    pipeline = JobDataPipeline()
    pipeline.run(job_title="Software Engineer", location="Leeds ", search_radius=10,
     max_pages=10)
    df = CreateJobDataFrame.create_blank_df()
    CreateJobDataFrame.insert_mutliple_job_information_objects_into_df(df, 
        pipeline.formatted_results)
    save_df_to_csv(df, "test_software_engineer_leeds_10_miles")
    