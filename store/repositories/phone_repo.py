from . import BaseRepository
from store.models.phone import Phone

class PhoneRepository(BaseRepository):
    
    @property
    def model(self) -> Phone:
        return Phone