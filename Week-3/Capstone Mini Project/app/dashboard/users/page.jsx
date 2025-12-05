export const metadata = {
    title: "Users — Launchpad Week 3",
    description: "User management page for the Launchpad Week 3 dashboard — displays a searchable, paginated user list with profile details and management actions.",
    keywords: ["users", "user management", "user list", "profiles", "dashboard", "react", "nextjs"],
    authors: [{ name: "Arpit Saxena" }],
};

import SmartTable from "@/components/ui/smartTable";
export default function Users() {
    return (
        <div>
            <SmartTable />
        </div>
    );
}