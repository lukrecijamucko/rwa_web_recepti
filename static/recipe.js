document.addEventListener("DOMContentLoaded", function () {
    const ingredientsContainer =
        document.getElementById("ingredients-container");

    const addIngredientButton =
        document.getElementById("add-ingredient");

    if (!ingredientsContainer || !addIngredientButton) {
        return;
    }

    addIngredientButton.addEventListener("click", function () {
        const input = document.createElement("input");

        input.type = "text";
        input.name = "ingredients";
        input.placeholder = "npr. brašno";

        ingredientsContainer.appendChild(input);
    });
});