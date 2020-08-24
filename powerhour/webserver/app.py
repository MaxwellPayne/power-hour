import asyncio
import uuid

from fastapi import FastAPI

import powerhour.webserver.executor
from powerhour.generation import generate_powerhour
from powerhour.webserver.db import database, generate_power_hour_jobs
from powerhour.webserver.models import GeneratePowerHourJob, GeneratePowerHourRequest
from powerhour.webserver.progress_logger import ProgressPercentageLogger


app = FastAPI()


@app.post('/generate', response_model=GeneratePowerHourJob)
async def generate(generate_request: GeneratePowerHourRequest):
    job = GeneratePowerHourJob(
        id=str(uuid.uuid4()),
        playlist_url=generate_request.playlist_url,
    )
    await database.execute(generate_power_hour_jobs.insert().values(
        youtube_api_key=generate_request.youtube_api_key,
        **job.dict(),
    ))

    loop = asyncio.get_event_loop()
    loop.run_in_executor(
        powerhour.webserver.executor.executor,
        generate_powerhour,
        job.playlist_url,
        generate_request.youtube_api_key,
        ProgressPercentageLogger(job.id),
    )
    return job


@app.get('/jobs/{job_id}', response_model=GeneratePowerHourJob)
async def get_job(job_id: str):
    query = generate_power_hour_jobs.select(generate_power_hour_jobs.c.id == job_id)
    return await database.fetch_one(query)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
