// JavaScript to dynamically add order item forms
document.addEventListener("DOMContentLoaded", function () {
  // Check if we're on the order creation page
  const addBtn = document.getElementById("add-item");
  const formsetArea = document.getElementById("formset-area");
  const totalForms = document.getElementById("id_orderitem_set-TOTAL_FORMS");

  if (addBtn && formsetArea && totalForms) {
    addBtn.addEventListener("click", function () {
      // Step 1: Get current form count
      const currentCount = parseInt(totalForms.value);

      // Step 2: Clone the last form in the formset
      const lastForm = formsetArea.querySelector(".formset-form:last-child");
      const newForm = lastForm.cloneNode(true);

      // Step 3: Clear input values in the cloned form
      const inputs = newForm.querySelectorAll("input, select, textarea");
      inputs.forEach(function (input) {
        if (input.type !== "hidden") {
          input.value = ""; // reset visible fields
        }
      });

      // Step 4: Update the name and id of each field to match the new form index
      inputs.forEach(function (input) {
        if (input.name) {
          const parts = input.name.split("-");
          parts[1] = currentCount; 
          input.name = parts.join("-");
        }
        if (input.id) {
          const parts = input.id.split("-");
          parts[1] = currentCount;
          input.id = parts.join("-");
        }
      });

      // Step 5: Append the new form and update TOTAL_FORMS
      formsetArea.appendChild(newForm);
      totalForms.value = currentCount + 1;
    });
  }
});