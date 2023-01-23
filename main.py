from src.df import SaveToDataFrame
from src.pipeline import JobDataPipeline

if __name__ == "__main__":
    pipeline = JobDataPipeline()
    pipeline.run(job_title="software-engineer", location="leeds", search_radius=10,
     max_pages=10)
    df = SaveToDataFrame.create_blank_df()
    SaveToDataFrame.insert_mutliple_job_information_objects_into_df(df, 
        pipeline.formatted_results)
    
