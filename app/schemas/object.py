import voltar as v
from voltar.pydantic_converter import convert_object

class Object(v.Object):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pydantic_model(self, name: str = None):
        """Convert the object to a Pydantic model.

        Args:
            name (str, optional): The name of the Pydantic model. Defaults to None.

        Returns:
            pydantic.BaseModel: The Pydantic model.
        """
        return convert_object(self, model_name=name)