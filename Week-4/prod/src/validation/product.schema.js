import Joi from "joi";

export const createProductSchema = Joi.object({
    name: Joi.string().min(2).required(),
    description: Joi.string().allow(""),
    price: Joi.number().min(0).required(),
    rating: Joi.number().min(0).max(5).default(0),
});
