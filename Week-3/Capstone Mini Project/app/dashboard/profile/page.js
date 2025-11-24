import ProfileDetail from "@/components/ui/ProfileDetails";

export default function Page() {
    return (
        <ProfileDetail
            image="/myimage.jpg"
            name="Arpit Saxena"
            jobTitle="Employee"
            email="arpitsaxena@example.com"
            linkedin="https://linkedin.com"
            twitter="https://www.x.com"
            facebook="https://facebook.com"
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
        />
    );
}
export const metadata = {
    title: "Users Page",
    description: "Capstone mini project — admin dashboard with reusable UI components.",
    keywords: "dashboard,nextjs,tailwind,charts,ui",
    authors: [{ name: "Arpit Saxena" }],
};
