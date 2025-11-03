export async function sendLoginRequest(data) {
  try {
    let res = await fetch("http://localhost:8000/login", {
      method: "POST",
      body: JSON.stringify(data)
    });
    return res;
  } catch (er) {
    console.error(er);
    return null;
  }
}
