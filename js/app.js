document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".waitlist-form");

    if (!form) return;

    const messageBox = document.getElementById("waitlist-message");

    const submitBtn = form.querySelector("button");

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        messageBox.innerHTML = "";

        submitBtn.disabled = true;
        submitBtn.textContent = "Reserving...";

        try {

            const formData = new FormData(form);

            const response = await fetch("/api/reserve", {

                method: "POST",

                body: formData

            });

            const data = await response.json();

            if (response.ok && data.success) {

                messageBox.innerHTML = `
                    <div class="success-box">

                        <strong>🎉 Welcome to Lionex Early Access</strong>

                        <br><br>

                        Your username
                        <strong>@${formData.get("username")}</strong>
                        has been successfully reserved.

                        <br><br>

                        A beautiful confirmation email has been sent to your inbox.

                        <br>

                        We'll notify you when Lionex officially launches.

                    </div>
                `;

                form.reset();

            } else {

                messageBox.innerHTML = `
                    <div class="error-box">

                        ❌ ${data.message || "Something went wrong."}

                    </div>
                `;

            }

        } catch (error) {

            console.error("Request Error:", error);

            messageBox.innerHTML = `
                <div class="error-box">

                    ❌ Unable to connect to the Lionex server.

                    <br>

                    Please try again in a few moments.

                </div>
            `;

        } finally {

            submitBtn.disabled = false;
            submitBtn.textContent = "Reserve My Username";

        }

    });

});
