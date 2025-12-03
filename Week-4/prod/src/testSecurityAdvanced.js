const BASE_URL = "http://localhost:5000/products";

//helpers
async function postJSON(url, data, headers = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...headers },
    body: JSON.stringify(data),
  });
  const json = await res.json().catch(() => ({}));
  return { status: res.status, json, headers: res.headers };
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

//testers

// CORS test
async function testCORS() {
  console.log("\nCORS Test");
  const allowed = await postJSON(
    BASE_URL,
    { name: "CORS Allowed", price: 10 },// these are simply the payloaders to send the example fields
    { Origin: "http://localhost:5000" } // header to check whether CORS is allowing or blocking exact heeaders or not
  );
  console.log("Allowed Origin Status:", allowed.status);

  await delay(500); // to give delay of 500 milliseconds

  const blocked = await postJSON(
    BASE_URL,
    { name: "CORS Blocked", price: 10 },
    { Origin: "http://evil.com" }
  );
  console.log("Blocked Origin Status:", blocked.status);
}

// Helmet headers test
async function testHelmetHeaders() {
  console.log("\nHelmet Headers Test");
  const res = await fetch(BASE_URL);
  console.log("Content-Security-Policy:", res.headers.get("content-security-policy"));
  console.log("X-Frame-Options:", res.headers.get("x-frame-options"));
  console.log("X-Content-Type-Options:", res.headers.get("x-content-type-options"));
  console.log("Referrer-Policy:", res.headers.get("referrer-policy"));
  console.log("Strict-Transport-Security:", res.headers.get("strict-transport-security"));
}

// Payload limit test
async function testPayloadLimit() {
  console.log("\nPayload Size Limit Test");
  // small payload
  let small = await postJSON(BASE_URL, { name: "Small", price: 10 });
  console.log("Small payload status:", small.status);

  await delay(200);

  // large payload (~1MB)
  const largeData = { name: "Large", price: 10, description: "A".repeat(1_000_000) };
  let large = await postJSON(BASE_URL, largeData);
  console.log("Large payload status:", large.status, "(Expect 413 Payload Too Large if configured)");
}

// nosql injection test
async function testNoSQLInjection() {
  console.log("\nNoSQL Injection Test");
  const payload = { name: { "$gt": "" }, price: 10 };
  const res = await postJSON(BASE_URL, payload);
  console.log("NoSQL Injection Status:", res.status, "Response:", res.json);
}

// XSS injection Test
async function testXSS() {
  console.log("\nXSS Injection Test");
  const payload = { name: "<script>alert('XSS')</script>", price: 10 };
  const res = await postJSON(BASE_URL, payload);
  console.log("XSS Injection Status:", res.status, "Response:", res.json);
}

// validation Test
async function testValidation() {
  console.log("\nValidation Bypass Test");
  const payload = { price: 10 }; // name parameter is missing
  const res = await postJSON(BASE_URL, payload);
  console.log("Validation Status:", res.status, "Response:", res.json);
}

// rate limiting test
async function testRateLimiting() {
  console.log("\nRate Limiting Test");
  const RATE_LIMIT_URL = "http://localhost:5000/products";

  for (let i = 1; i <= 10; i++) {
    const { status } = await postJSON(RATE_LIMIT_URL, { name: `Test ${i}`, price: 100 });
    console.log(`Request ${i}: Status ${status}`);
    await delay(100); // slight delay between requests
  }
}

async function runAllTests() {
  console.log("Running Security Tests in Isolation");

  console.log("\nStep 1: CORS Test (rate limiter bypassed)");
  await testCORS();

  console.log("\nStep 2: Helmet Headers Test");
  await testHelmetHeaders();

  console.log("\nStep 3: Payload Size Limit Test");
  await testPayloadLimit();

  console.log("\nStep 4: NoSQL Injection Test");
  await testNoSQLInjection();

  console.log("\nStep 5: XSS Injection Test");
  await testXSS();

  console.log("\nStep 6: Validation Test");
  await testValidation();

  console.log("\nStep 7: Rate Limiting Test (dedicated route only)");
  await testRateLimiting();

  console.log("\nAll tests completed!");
}

runAllTests();
