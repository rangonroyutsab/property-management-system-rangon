// Search autocomplete logic

(function () {
    const autocompleteUrl = document.body.dataset.autocompleteUrl;

    if (!autocompleteUrl) return;

    document.querySelectorAll(".autocomplete-input").forEach(function (input) {
        const wrapper = input.closest(".search-wrap, .listing-search-bar");
        if (!wrapper) return;

        const dropdown = wrapper.querySelector(".autocomplete-dropdown");
        if (!dropdown) return;

        let timer;

        function closeDropdown() {
            dropdown.classList.remove("open");
            dropdown.innerHTML = "";
        }

        input.addEventListener("input", function () {
            clearTimeout(timer);

            const query = input.value.trim();

            if (query.length < 2) {
                closeDropdown();
                return;
            }

            timer = setTimeout(function () {
                fetch(autocompleteUrl + "?q=" + encodeURIComponent(query))
                    .then(function (response) {
                        return response.json();
                    })
                    .then(function (locations) {
                        dropdown.innerHTML = "";

                        if (!locations.length) {
                            closeDropdown();
                            return;
                        }

                        locations.forEach(function (location) {
                            const item = document.createElement("button");
                            item.className = "autocomplete-item";
                            item.type = "button";

                            const icon = document.createElement("span");
                            icon.className = "ac-icon";
                            icon.setAttribute("aria-hidden", "true");

                            const text = document.createElement("span");
                            text.className = "ac-text";

                            const name = document.createElement("strong");
                            name.textContent = location.name;

                            const label = document.createElement("span");
                            label.textContent = "Location";

                            text.appendChild(name);
                            text.appendChild(label);
                            item.appendChild(icon);
                            item.appendChild(text);

                            item.addEventListener("click", function () {
                                input.value = location.name;
                                closeDropdown();

                                const form = input.closest("form");
                                if (form) form.submit();
                            });

                            dropdown.appendChild(item);
                        });

                        dropdown.classList.add("open");
                    })
                    .catch(function () {
                        closeDropdown();
                    });
            }, 250);
        });

        input.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeDropdown();
            }
        });

        document.addEventListener("click", function (event) {
            if (!wrapper.contains(event.target)) {
                closeDropdown();
            }
        });
    });
}());


(function () {
    const mainImage = document.getElementById("gallery-main-image");
    if (!mainImage) return;

    document.querySelectorAll(".gallery-thumb").forEach(function (thumb) {
        thumb.addEventListener("click", function () {
            const imageUrl = thumb.dataset.imageUrl;
            const imageAlt = thumb.dataset.imageAlt || "Property image";
            if (!imageUrl) return;

            mainImage.src = imageUrl;
            mainImage.alt = imageAlt;

            document.querySelectorAll(".gallery-thumb").forEach(function (item) {
                item.classList.remove("is-active");
            });
            thumb.classList.add("is-active");
        });
    });
}());
