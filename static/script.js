
document.addEventListener("DOMContentLoaded", function () {
    const completionForms = document.querySelectorAll(
        'form[action*="/complete"]'
    );

    completionForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = window.confirm(
                "Mark this collection as completed?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    const addForm = document.querySelector(
        'form[action*="/bins/add"]'
    );

    if (addForm) {
        addForm.addEventListener("submit", function (event) {
            const fillInput = addForm.querySelector(
                'input[name="fill_level"]'
            );

            const fill = Number(fillInput.value);

            if (!Number.isInteger(fill) || fill < 0 || fill > 100) {
                event.preventDefault();
                window.alert(
                    "Fill level must be a whole number from 0 to 100."
                );
            }
        });
    }
});
