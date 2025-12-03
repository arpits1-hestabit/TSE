import express from "express";

export default function loadMiddlewares(app) {
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
}
