
swagger_models_definitions = {
    "User" : {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
                "description": "User's id",
                "default": "Null"
            },
            "name": {
                "type": "string",
                "description": "User's name",
                "default": "John"
            },
            "additional_info": {
                "type": "string",
                "description": "User's additiona desc",
                "default": "Empty text"
            },
            "phones": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/Phone"
                }
            }
        }
    },


    "Phone": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
                "description": "Phone's name",
                "default": "Null"
            },
            "phone": {
                "type": "strine",
                "description": "Phone's number",
                "default": "+7-233-232-23-23"
            },
        }
    },

}