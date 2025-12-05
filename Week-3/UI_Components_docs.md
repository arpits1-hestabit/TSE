# Components Folder — Summary & Usage Examples

This file contain the components which are reusable along with their usage examples.

1. AreaChart.jsx
  - Small area chart built on Graph (Chart.js wrapper).
  - Example:
    ```jsx
    <AreaChart data={{ labels:["Jan"], datasets:[{data:[10], backgroundColor:"rgba(99,102,241,0.2)", borderColor:"#6366f1"}] }} height={160} />
    ```

 2. BarChart.jsx
  - Bar chart wrapper for categorical data.
  - Example:
    ```jsx
    <BarChart data={{ labels:["Q1"], datasets:[{data:[300], backgroundColor:"#10b981"}] }} />
    ```

 3. Graph.jsx
  - Generic Chart.js wrapper used by AreaChart/BarChart. Accepts type, data, options.
  - Example:
    ```jsx
    <Graph type="line" data={data} options={{ maintainAspectRatio: false }} />
    ```

 4. Table.jsx / smartTable.jsx
  - Table.jsx: lightweight table for small datasets (columns + data + rowKey).
    ```jsx
    <Table columns={[{key:"name",label:"Name"}]} data={[{id:1,name:"Alice"}]} />
    ```
  - smartTable.jsx: enhanced table (sorting/search/pagination) — check file for API.

 5. Input.jsx / label.jsx / button.jsx
  - Reusable form primitives with consistent styling and error handling.
    ```jsx
    <Input id="email" label="Email" value={val} onChange={e => setVal(e.target.value)} />
    <button className="btn" onClick={handle}>Save</button>
    ```

 6. Card.jsx / magic-card.jsx / hero.jsx / marquee.jsx
  - Visual layout components to group content or create hero/animated sections.
    ```jsx
    <Card title="Overview"><p>Content</p></Card>
    ```

 7. Navbar.jsx / Sidebar.jsx / Footer.jsx
  - Layout/navigation components for persistent header, side navigation, and footer.
    ```jsx
    <Sidebar items={[{href:"/dashboard",label:"Dashboard"}]} />
    <Navbar links={[{href:"/",label:"Home"}]} />
    ```

