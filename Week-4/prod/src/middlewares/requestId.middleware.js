import { randomUUID } from "crypto";

export const requestIdMiddleware = (req, res, next) => {
    const requestId = randomUUID(); // will generate request id
    req.requestId = requestId; // attach to request object
    res.setHeader("X-Request-ID", requestId); // will return as a response wuth body
    next();
};

