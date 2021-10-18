from . import BaseRepository
from store.models.role import Role

class RoleRepository(BaseRepository):
    
    @property
    def model(self) -> Role:
        return Role