import productService from "../services/product.service.js";

class ProductController {

    //creating product
    async create(req, res, next) {
        try {
            const product = await productService.create(req.body);

            return res.status(201).json({
                success: true,
                data: product,
            });
        } catch (err) {
            next(err);
        }
    }

    //finding all products(filter + pagination)
    async find(req, res, next) {
        try {
            const result = await productService.find(req.query);

            return res.json({
                success: true,
                ...result, 
            });
        } catch (err) {
            next(err);
        }
    }

    // finding product by id 
    async findById(req, res, next) {
        try {
            const product = await productService.findById(req.params.id, req.query);

            return res.json({
                success: true,
                data: product,
            });
        } catch (err) {
            next(err);
        }
    }

    // update product
    async update(req, res, next) {
        try {
            const updated = await productService.update(req.params.id, req.body);

            return res.json({
                success: true,
                data: updated,
            });
        } catch (err) {
            next(err);
        }
    }

    //soft delete
    async softDelete(req, res, next) {
        try {
            const result = await productService.softDelete(req.params.id);

            return res.json({
                success: true,
                data: result,
            });
        } catch (err) {
            next(err);
        }
    }
}

export default new ProductController();
