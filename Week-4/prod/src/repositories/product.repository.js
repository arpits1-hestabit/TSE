import Product from "../models/product.js";
export default class ProductRepository {
    async create(data) {
        const product = new Product(data);
        return await product.save();
    }

    async findById(id) {
        return Product.findById(id);
    }

    async findPaginated({ page = 1, limit = 10, filter = {} }) {
        const skip = (page - 1) * limit;

        const data = await Product.find(filter)
            .skip(skip)
            .limit(limit)
            .sort({ createdAt: -1 });

        const total = await Product.countDocuments(filter);

        return {
            data,
            pagination: {
                page,
                limit,
                total,
                totalPages: Math.ceil(total / limit),
            },
        };
    }

    async update(id, updates) {
        return Product.findByIdAndUpdate(id, updates, {
            new: true,
            runValidators: true,
        });
    }

    async delete(id) {
        return Product.findByIdAndDelete(id);
    }
}
