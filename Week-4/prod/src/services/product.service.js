import Product from "../models/product.js";

class ProductService {
    async create(data) {
        return await Product.create(data);
    }

    async find(query) {
        const {
            search,
            status,
            minPrice,
            maxPrice,
            sort = "createdAt:-1",
            page = 1,
            limit = 10,
            includeDeleted = false,
        } = query;

        const filter = {};

        if (!includeDeleted) filter.deletedAt = null;// logic for soft delete

        if (search) { // dynamic search
            filter.$or = [
                { name: new RegExp(search, "i") },
                { description: new RegExp(search, "i") }
            ];
        }

        if (minPrice || maxPrice) { // price filtering
            filter.price = {};
            if (minPrice) filter.price.$gte = Number(minPrice);
            if (maxPrice) filter.price.$lte = Number(maxPrice);
        }

        if (status) {  // Status filtering
            filter.status = status;
        }

        // Sorting
        const [sortField, sortOrder] = sort.split(":");
        const sortObj = { [sortField]: Number(sortOrder) };

        const skip = (page - 1) * limit;

        const items = await Product.find(filter)
            .sort(sortObj)
            .skip(skip)
            .limit(Number(limit));

        const total = await Product.countDocuments(filter);

        return {
            data: items,
            pagination: {
                total,
                page: Number(page),
                limit: Number(limit),
                totalPages: Math.ceil(total / limit),
            },
        };
    }

    async findById(id, query) {
        const product = await Product.findById(id);

        if (!product) throw new Error("Product not found");

        if (!query.includeDeleted && product.deletedAt) {
            throw new Error("Product has been deleted");
        }

        return product;
    }

    async update(id, data) {
        const product = await Product.findByIdAndUpdate(id, data, {
            new: true,
            runValidators: true,
        });

        if (!product) throw new Error("Product not found");

        return product;
    }

    async softDelete(id) {
        const product = await Product.findByIdAndUpdate(
            id,
            { deletedAt: new Date() },
            { new: true }
        );

        if (!product) throw new Error("Product not found");

        return product;
    }
}

export default new ProductService();
