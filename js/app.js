document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".waitlist-form");

    if (!form) return;

    const messageBox =
        document.getElementById("waitlist-message");

    const submitBtn =
        form.querySelector("button");

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        messageBox.innerHTML = "";

        submitBtn.disabled = true;
        submitBtn.textContent = "Reserving...";

        try {

            const formData = new FormData(form);

            const response = await fetch("/reserve", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (data.success) {

                messageBox.innerHTML = `
                    <div class="success-box">
                        <strong>🎉 Welcome to Lionex Early Access</strong>
                        <br><br>
                        Your username <strong>@${formData.get("username")}</strong>
                        has been successfully reserved.
                        <br>
                        We'll notify you when Lionex launches.
                    </div>
                `;

                form.reset();

            } else {

                messageBox.innerHTML = `
                    <div class="error-box">
                        ❌ ${data.message}
                    </div>
                `;
            }

        } catch (error) {

            console.error(error);

            messageBox.innerHTML = `
                <div class="error-box">
                    ❌ Unable to connect to the server.
                    Please try again later.
                </div>
            `;

        } finally {

            submitBtn.disabled = false;
            submitBtn.textContent = "Reserve My Username";

        }

    });

});
