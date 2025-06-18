console.log("Script de arriendo cargado correctamente");

document.addEventListener("DOMContentLoaded", function() {
    const elements = {
        bicicletaSelect: document.getElementById('id_bicicleta'),
        fechaInicioInput: document.getElementById('id_fecha_inicio'),
        fechaFinInput: document.getElementById('id_fecha_fin'),
        costoArriendoInput: document.getElementById('formatted_costo_arriendo'),
        depositoGarantiaInput: document.getElementById('formatted_deposito_garantia'),
        costoTotalInput: document.getElementById('formatted_costo_total'),
        bicicletaPreview: document.getElementById('bicicleta-preview')
    };

    const DEPOSITO_GARANTIA = 100000;  // Monto fijo de depósito de garantía

    function initializeFlatpickr() {
        if (typeof flatpickr !== "function") {
            console.error("Flatpickr no está cargado correctamente");
            return;
        }

        const flatpickrConfig = {
            dateFormat: "Y-m-d",
            minDate: "today",
            onChange: updateCosts,
            onClose: function(selectedDates, dateStr, instance) {
                if (selectedDates[0]) {
                    let formattedDate = selectedDates[0].toISOString().split('T')[0];
                    instance.input.setAttribute('data-date', formattedDate);
                }
            }
        };

        flatpickr(elements.fechaInicioInput, flatpickrConfig);
        flatpickr(elements.fechaFinInput, flatpickrConfig);
    }

    function updateCosts() {
        const selectedOption = elements.bicicletaSelect.options[elements.bicicletaSelect.selectedIndex];
        const precioPorDia = parseInt(selectedOption.getAttribute('data-precio')) || 0;
        const fechaInicio = new Date(elements.fechaInicioInput.value);
        const fechaFin = new Date(elements.fechaFinInput.value);
    
        if (fechaInicio && fechaFin && fechaInicio < fechaFin) {
            const diffDays = Math.ceil((fechaFin - fechaInicio) / (1000 * 60 * 60 * 24));
            const costoArriendo = Math.round(precioPorDia * diffDays);
            const costoTotal = costoArriendo + DEPOSITO_GARANTIA;
    
            // Actualiza los inputs visibles
            elements.costoArriendoInput.value = formatCurrency(costoArriendo);
            elements.depositoGarantiaInput.value = formatCurrency(DEPOSITO_GARANTIA);
            elements.costoTotalInput.value = formatCurrency(costoTotal);
    
            // Actualiza los campos ocultos que se enviarán
            document.getElementById('id_costo_arriendo').value = costoArriendo;
            document.getElementById('id_deposito_garantia').value = DEPOSITO_GARANTIA;
            document.getElementById('id_costo_total').value = costoTotal;
        } else {
            clearCostFields();
        }
    }
    
    function clearCostFields() {
        ['id_costo_arriendo', 'id_deposito_garantia', 'id_costo_total', 'formatted_costo_arriendo', 'formatted_deposito_garantia', 'formatted_costo_total'].forEach(id => {
            document.getElementById(id).value = '';
        });
    }

    function formatCurrency(amount) {
        return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(amount);
    }

    function updateBicicletaPreview() {
        const selectedOption = elements.bicicletaSelect.options[elements.bicicletaSelect.selectedIndex];
        const imagenUrl = selectedOption.getAttribute('data-imagen-url');
        elements.bicicletaPreview.src = imagenUrl || '';
        elements.bicicletaPreview.classList.toggle('hidden', !imagenUrl);
    }

    function initialize() {
        initializeFlatpickr();
        updateBicicletaPreview();
        elements.bicicletaSelect.addEventListener('change', () => {
            updateBicicletaPreview();
            updateCosts();
        });
        elements.fechaInicioInput.addEventListener('change', updateCosts);
        elements.fechaFinInput.addEventListener('change', updateCosts);
    }

    initialize();
});