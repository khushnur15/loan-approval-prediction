document.getElementById("loanForm").addEventListener(
    "submit",
    async function (e) {

        e.preventDefault();

        const data = {
            Gender: parseInt(document.getElementById("Gender").value),
            Married: parseInt(document.getElementById("Married").value),
            Dependents: parseInt(document.getElementById("Dependents").value),
            Education: parseInt(document.getElementById("Education").value),
            Self_Employed: parseInt(document.getElementById("Self_Employed").value),
            ApplicantIncome: parseInt(document.getElementById("ApplicantIncome").value),
            CoapplicantIncome: parseInt(document.getElementById("CoapplicantIncome").value),

            // convert rupees to dataset scale
            LoanAmount: Math.round(
                parseInt(
                    document.getElementById("LoanAmount").value
                ) / 1000
            ),

            Loan_Amount_Term: parseInt(
                document.getElementById("Loan_Amount_Term").value
            ),

            Credit_History: parseInt(
                document.getElementById("Credit_History").value
            ),

            Property_Area: parseInt(
                document.getElementById("Property_Area").value
            )
        };

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/predict",
                {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }
            );

            const result = await response.json();

            localStorage.setItem(
                "loanResult",
                JSON.stringify(result)
            );

            window.location.href = "/result";

        } catch (error) {

            console.log(error);

            alert(
                "Unable to connect to backend server."
            );
        }
    }
);