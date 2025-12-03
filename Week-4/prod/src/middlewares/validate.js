import Joi from "joi";

// Middleware
export const validate = (schema) => (req, res, next) => {
    const options = { abortEarly: false, allowUnknown: false, stripUnknown: true };
    const { error, value } = schema.validate(req.body, options);
    if (error) {
        return res.status(400).json({
            success: false,
            message: "Validation failed",
            details: error.details.map(d => d.message),
            timestamp: new Date().toISOString(),
            path: req.originalUrl,
        });
    }
    req.body = value;
    next();
};

// User schema
export const registerUserSchema = Joi.object({
    firstName: Joi.string().trim().min(2).required(),
    lastName: Joi.string().trim().min(2).required(),
    email: Joi.string().trim().lowercase().email({ minDomainSegments: 2 }).required(),
    password: Joi.string().min(6).required()
});

export const loginUserSchema = Joi.object({
    email: Joi.string().trim().lowercase().email().required(),
    password: Joi.string().min(6).required()
});

export const updateUserSchema = Joi.object({
    firstName: Joi.string().trim().min(2),
    lastName: Joi.string().trim().min(2),
    email: Joi.string().trim().lowercase().email(),
    password: Joi.string().min(6)
}).min(1);

// Product schema
export const createProductSchema = Joi.object({
    name: Joi.string().trim().min(2).required(),
    description: Joi.string().trim().allow("", null),
    price: Joi.number().min(0).precision(2).required(),
    rating: Joi.number().min(0).max(5).default(0)
});

export const updateProductSchema = Joi.object({
    name: Joi.string().trim().min(2),
    description: Joi.string().trim().allow("", null),
    price: Joi.number().min(0).precision(2),
    rating: Joi.number().min(0).max(5)
}).min(1);
