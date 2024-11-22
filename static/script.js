// Funcion para convertir markdown a html
function markdownToHtml(markdown) {
    const converter = new showdown.Converter();
    return converter.makeHtml(markdown);
}

// Buscar receta
function searchRecipe() {
    const recipeId = document.getElementById('search_recipe_id').value;

    fetch('/search_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipe_id: recipeId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Recipe not found');
        }
        return response.json();
    })
    .then(recipe => {
        // Mostrar los datos en los campos
        document.getElementById('title').value = recipe.title;
        document.getElementById('ingredients').value = recipe.ingredients;
        document.getElementById('steps').value = recipe.steps;
    })
    .catch(error => {
        alert(error.message);
    });
}

// Analizar receta por ID
function analyzeRecipe() {
    const recipeId = document.getElementById('recipe_id').value;

    if (recipeId.trim() === "") {
        alert("Por favor, ingresa un ID de receta válido.");
        return;
    }

    // Enviar a backend
    fetch('/analyze_recipe', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({recipe_id: recipeId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Convert Llama response from Markdown to HTML
            const formattedResponse = markdownToHtml(data.llama_response);
            // Agregar titulo y formatear respuesta
            document.getElementById('chatbox').innerHTML += `
                <h3>Resultados del Análisis para Receta ID ${recipeId}</h3>
                <p>${formattedResponse.replace(/\n/g, '</p><p>')}</p>`;
        }
    })
    .catch(error => {
        console.error("Error al analizar la receta por ID:", error);
    });
}

// Analizar rango de recetas
function analyzeRange() {
    const rangeStart = document.getElementById('range_start').value;
    const rangeEnd = document.getElementById('range_end').value;

    if (rangeStart.trim() === "" || rangeEnd.trim() === "") {
        alert("Por favor, ingresa un rango válido.");
        return;
    }

    // Enviar a backend
    fetch('/analyze_range', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({range_start: rangeStart, range_end: rangeEnd})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Convert Llama response from Markdown to HTML
            const formattedResponse = markdownToHtml(data.llama_response);
            // Add the title and formatted response
            document.getElementById('chatbox').innerHTML += `
                <h3>Resultados del Análisis para Recetas en Rango ${rangeStart} a ${rangeEnd}</h3>
                <p>${formattedResponse.replace(/\n/g, '</p><p>')}</p>`;
        }
    })
    .catch(error => {
        console.error("Error al analizar el rango de recetas:", error);
    });
}

// Analizar receta por texto
function customAnalyze() {
    const customMessage = document.getElementById('custom_message').value;

    if (customMessage.trim() === "") {
        alert("Por favor, ingresa un mensaje personalizado.");
        return;
    }

    // Enviar a backend
    fetch("/analizar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: customMessage
        })
    })
    .then(response => response.json())
    .then(data => {
        const llamaResponseHtml = markdownToHtml(data.result);
        const llamaResponseDiv = document.getElementById("chatbox");
        llamaResponseDiv.innerHTML += `<h3>Resultados del Análisis</h3>`;
        llamaResponseDiv.innerHTML += `<p>${llamaResponseHtml.replace(/\n/g, '</p><p>')}</p>`;
    })
    .catch(error => {
        console.error("Error al analizar la receta:", error);
    });
}

// Buscar receta pro ID
function searchRecipe() {
    const searchRecipeId = document.getElementById('search_recipe_id').value;

    if (searchRecipeId.trim() === "") {
        alert("Por favor, ingresa un ID de receta válido para buscar.");
        return;
    }

    // enviar a backend
    fetch('/search_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ recipe_id: searchRecipeId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Receta no encontrada.");
        } else {
            // mostrar datos de la busqueda en front
            document.getElementById('title').value = data.title;
            document.getElementById('ingredients').value = data.ingredients;
            document.getElementById('steps').value = data.steps;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// Actualizar receta
function updateRecipe() {
    const recipeId = document.getElementById('search_recipe_id').value;
    const title = document.getElementById('title').value;
    const ingredients = document.getElementById('ingredients').value;
    const steps = document.getElementById('steps').value;

    fetch('/update_recipe', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({recipe_id: recipeId, title, ingredients, steps})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.success ? "Receta actualizada exitosamente." : "Error al actualizar la receta.");
    })
    .catch(error => {
        console.error("Error al actualizar la receta:", error);
    });
}

// Borrar receta
function deleteRecipe() {
    const recipeId = document.getElementById('search_recipe_id').value;

    fetch('/delete_recipe', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({recipe_id: recipeId})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.success ? "Receta eliminada exitosamente." : "Error al eliminar la receta.");
    })
    .catch(error => {
        console.error("Error al eliminar la receta:", error);
    });
}

// Agregar receta
function addRecipe() {
    const title = document.getElementById('new_title').value;
    const ingredients = document.getElementById('new_ingredients').value;
    const steps = document.getElementById('new_steps').value;

    fetch('/add_recipe', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title, ingredients, steps})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.success ? "Receta agregada exitosamente." : "Error al agregar la receta.");
    })
    .catch(error => {
        console.error("Error al agregar la receta:", error);
    });
}