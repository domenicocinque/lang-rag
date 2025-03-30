from pydantic import BaseModel


class StammeringCheckResponse(BaseModel):
    has_stammer: bool
