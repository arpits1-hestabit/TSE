# UI Component Docs — Usage Examples

This document lists the UI components in components/ui with props, behavior notes, and example usage. Import paths assume:
import X from "components/ui/X.jsx"

Notes
- Client components (interactive/chart components) must include "use client" at top of the file that consumes them (Next.js App Router).
- Examples use JSX; adapt to your project structure if necessary.

----


## AreaChart.jsx
Purpose: Small area chart wrapper (uses Chart.js via a Graph wrapper).

Props:
- data: required — { labels: string[], datasets: Array<{ label?: string, data: number[], backgroundColor?: string, borderColor?: string }> }
- options: optional — Chart.js options object
- height: optional — number

Example:
```jsx
// Example usage
import AreaChart from "components/ui/AreaChart.jsx";

const data = {
  labels: ["Jan", "Feb", "Mar"],
  datasets: [{ label: "Sales", data: [10, 20, 15], backgroundColor: "rgba(99, 102, 241, 0.2)", borderColor: "#6366f1" }]
};

export default function Dashboard() {
  return <AreaChart data={data} options={{ maintainAspectRatio: false }} height={200} />;
}


BarChart.jsx
Purpose: Bar chart wrapper for categorical comparisons.

Props:

data: required — same shape as AreaChart
options: optional — Chart.js options
height: optional — number
Example:

import BarChart from "components/ui/BarChart.jsx";

const data = {
  labels: ["Q1", "Q2", "Q3"],
  datasets: [{ label: "Revenue", data: [300, 500, 400], backgroundColor: "#10b981" }]
};

export default function Stats() {
  return <BarChart data={data} options={{ scales: { y: { beginAtZero: true } } }} />;
}



Graph.jsx
Purpose: Generic chart wrapper used by AreaChart/BarChart. Exposes Chart.js directly.

Props:

type: required — "line" | "bar" | "pie" | ...
data: required
options: optional
height: optional
Example:



import Graph from "components/ui/Graph.jsx";

const data = { labels: ["A","B"], datasets: [{ data: [1,2] }] };

export default function Example() {
  return <Graph type="line" data={data} />;
}



Table.jsx
Purpose: Simple data table used for lists and small datasets.

Props:

columns: required — Array<{ key: string, label: string, render?: (row)=>JSX }>
data: required — Array<object>
rowKey: optional — string (defaults to "id")
Example:


import Table from "components/ui/Table.jsx";

const columns = [
  { key: "name", label: "Name" },
  { key: "email", label: "Email" },
  { key: "actions", label: "Actions", render: (row)=> <button onClick={()=>alert(row.id)}>View</button> }
];

const data = [{ id: 1, name: "Alice", email: "a@example.com" }];

export default function Users() {
  return <Table columns={columns} data={data} rowKey="id" />;
}



Input.jsx
Purpose: Reusable input field with label and error display.

Props:

id: optional — string
label: optional — string
value: optional — string
onChange: required — function
type: optional — "text" | "email" | "password" (default "text")
placeholder: optional
error: optional — string
Example:



import Input from "components/ui/Input.jsx";
import { useState } from "react";

export default function Form() {
  const [email, setEmail] = useState("");
  return (
    <Input id="email" label="Email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" />
  );
}



BarChart.jsx
Purpose: Bar chart wrapper for categorical comparisons.

Props:

data: required — same shape as AreaChart
options: optional — Chart.js options
height: optional — number
Example:

Graph.jsx
Purpose: Generic chart wrapper used by AreaChart/BarChart. Exposes Chart.js directly.

Props:

type: required — "line" | "bar" | "pie" | ...
data: required
options: optional
height: optional
Example:

Table.jsx
Purpose: Simple data table used for lists and small datasets.

Props:

columns: required — Array<{ key: string, label: string, render?: (row)=>JSX }>
data: required — Array<object>
rowKey: optional — string (defaults to "id")
Example:

Input.jsx
Purpose: Reusable input field with label and error display.

Props:

id: optional — string
label: optional — string
value: optional — string
onChange: required — function
type: optional — "text" | "email" | "password" (default "text")
placeholder: optional
error: optional — string
Example:

Button.jsx
Purpose: Primary button with size and variant control.

Props:

children: required — node
onClick: optional — function
variant: optional — "primary" | "secondary" (default "primary")
size: optional — "sm" | "md" | "lg" (default "md")
disabled: optional — boolean
Example:



import Button from "components/ui/Button.jsx";

export default function Actions() {
  return <Button variant="primary" onClick={()=>console.log("clicked")}>Save</Button>;
}

Card.jsx
Purpose: Simple card container with header and body slots.

Props:

title: optional — string | node
children: required — content
footer: optional — node
Example:


import Card from "components/ui/Card.jsx";

export default function InfoCard() {
  return (
    <Card title="Overview" footer={<small>Updated today</small>}>
      <p>Key metrics and summary go here.</p>
    </Card>
  );
}



BarChart.jsx
Purpose: Bar chart wrapper for categorical comparisons.

Props:

data: required — same shape as AreaChart
options: optional — Chart.js options
height: optional — number
Example:

Graph.jsx
Purpose: Generic chart wrapper used by AreaChart/BarChart. Exposes Chart.js directly.

Props:

type: required — "line" | "bar" | "pie" | ...
data: required
options: optional
height: optional
Example:

Table.jsx
Purpose: Simple data table used for lists and small datasets.

Props:

columns: required — Array<{ key: string, label: string, render?: (row)=>JSX }>
data: required — Array<object>
rowKey: optional — string (defaults to "id")
Example:

Input.jsx
Purpose: Reusable input field with label and error display.

Props:

id: optional — string
label: optional — string
value: optional — string
onChange: required — function
type: optional — "text" | "email" | "password" (default "text")
placeholder: optional
error: optional — string
Example:

Button.jsx
Purpose: Primary button with size and variant control.

Props:

children: required — node
onClick: optional — function
variant: optional — "primary" | "secondary" (default "primary")
size: optional — "sm" | "md" | "lg" (default "md")
disabled: optional — boolean
Example:

Card.jsx
Purpose: Simple card container with header and body slots.

Props:

title: optional — string | node
children: required — content
footer: optional — node
Example:

Badge.jsx
Purpose: Small inline status/label component.

Props:

children: required — node
variant: optional — "default" | "success" | "danger" (default "default")
Example:


import Badge from "components/ui/Badge.jsx";

export default function Status() {
  return <Badge variant="success">Active</Badge>;
}









Modal.jsx
Purpose: Controlled modal dialog.

Props:

open: required — boolean
onClose: required — function
title: optional — string | node
children: required — node
Usage notes: Modal likely requires portal or top-level placement; ensure only one open at a time.

Example:




import Modal from "components/ui/Modal.jsx";
import { useState } from "react";

export default function ExampleModal() {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button onClick={()=>setOpen(true)}>Open</button>
      <Modal open={open} onClose={()=>setOpen(false)} title="Details">
        <p>Modal content</p>
      </Modal>
    </>
  );
}


BarChart.jsx
Purpose: Bar chart wrapper for categorical comparisons.

Props:

data: required — same shape as AreaChart
options: optional — Chart.js options
height: optional — number
Example:

Graph.jsx
Purpose: Generic chart wrapper used by AreaChart/BarChart. Exposes Chart.js directly.

Props:

type: required — "line" | "bar" | "pie" | ...
data: required
options: optional
height: optional
Example:

Table.jsx
Purpose: Simple data table used for lists and small datasets.

Props:

columns: required — Array<{ key: string, label: string, render?: (row)=>JSX }>
data: required — Array<object>
rowKey: optional — string (defaults to "id")
Example:

Input.jsx
Purpose: Reusable input field with label and error display.

Props:

id: optional — string
label: optional — string
value: optional — string
onChange: required — function
type: optional — "text" | "email" | "password" (default "text")
placeholder: optional
error: optional — string
Example:

Button.jsx
Purpose: Primary button with size and variant control.

Props:

children: required — node
onClick: optional — function
variant: optional — "primary" | "secondary" (default "primary")
size: optional — "sm" | "md" | "lg" (default "md")
disabled: optional — boolean
Example:

Card.jsx
Purpose: Simple card container with header and body slots.

Props:

title: optional — string | node
children: required — content
footer: optional — node
Example:

Badge.jsx
Purpose: Small inline status/label component.

Props:

children: required — node
variant: optional — "default" | "success" | "danger" (default "default")
Example:

Modal.jsx
Purpose: Controlled modal dialog.

Props:

open: required — boolean
onClose: required — function
title: optional — string | node
children: required — node
Usage notes: Modal likely requires portal or top-level placement; ensure only one open at a time.

Example:

Navbar.jsx
Purpose: Top navigation bar. Accepts children or links prop.

Props:

children: optional — node
links: optional — Array<{ href, label }>
Example:


import Navbar from "components/ui/Navbar.jsx";

export default function TopNav() {
  const links = [{ href: "/", label: "Home" }, { href: "/dashboard", label: "Dashboard" }];
  return <Navbar links={links} />;
}


Sidebar.jsx
Purpose: Persistent navigation sidebar for the dashboard.

Props:

items: required — Array<{ href, label, icon?: node }>
collapsed: optional — boolean
Example:





import Sidebar from "components/ui/Sidebar.jsx";

const items = [{ href: "/dashboard", label: "Dashboard" }, { href: "/dashboard/profile", label: "Profile" }];

export default function Layout() {
  return (
    <div className="app-grid">
      <Sidebar items={items} />
      <main>/* page content */</main>
    </div>
  );
}

Tips and gotchas

Charts: Charts and other DOM-manipulating components must be client components in Next.js. Use "use client" in the consuming file.
Styles: Components rely on global CSS (app/globals.css). If classes look off, verify Tailwind/PostCSS build in next.config.mjs.
Accessibility: Ensure inputs have labels/aria attributes for screen readers.
Table: For large datasets, implement virtualization or pagination.





