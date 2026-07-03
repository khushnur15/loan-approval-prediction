document.getElementById("loanForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        Gender: parseInt(document.getElementById("Gender").value),
        Married: parseInt(document.getElementById("Married").value),
        Dependents: parseInt(document.getElementById("Dependents").value),
        Education: parseInt(document.getElementById("Education").value),
        Self_Employed: parseInt(document.getElementById("Self_Employed").value),
        ApplicantIncome: parseInt(document.getElementById("ApplicantIncome").value),
        CoapplicantIncome: parseInt(document.getElementById("CoapplicantIncome").value),
        LoanAmount: parseInt(document.getElementById("LoanAmount").value),
        Loan_Amount_Term: parseInt(document.getElementById("Loan_Amount_Term").value),
        Credit_History: parseInt(document.getElementById("Credit_History").value),
        Property_Area: parseInt(document.getElementById("Property_Area").value)
    };

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("result").innerText =
        "Prediction: " + result.prediction;
});