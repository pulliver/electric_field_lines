// Canvas dimensions
const width = 600, height = 600;

// Position and magnitude of the charge
const charge = { x: 300, y: 300, q: 1 }; // 1 Coulomb at (300, 300)

// Coulomb's constant
const k = 8.987e9;

// Reference distance (20 pixels from the charge)
const referenceDistance = 20;

// Normalized scaling factor
const normalized = 10; // You can tweak this value later

// Fixed arrow length at the reference distance
const fixedArrowLength = width / normalized;

// Calculate the electric field magnitude at the reference distance
const referenceFieldMagnitude = k * charge.q / (referenceDistance ** 2);

// Add the SVG canvas
const svg = d3.select("#canvas");

// Add arrow marker definition
svg.append("defs")
    .append("marker")
    .attr("id", "arrow")
    .attr("viewBox", "0 0 10 10")
    .attr("refX", 5)
    .attr("refY", 5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M 0 0 L 10 5 L 0 10 Z")
    .attr("fill", "black");

// Function to calculate the electric field
function calculateField(q, cx, cy, x, y) {
    const dx = x - cx;
    const dy = y - cy;
    const rSquared = dx ** 2 + dy ** 2;
    const r = Math.sqrt(rSquared);

    if (r === 0) return { fx: 0, fy: 0, magnitude: 0 }; // Avoid division by zero

    const magnitude = k * q / rSquared; // Coulomb's law
    return { fx: magnitude * dx / r, fy: magnitude * dy / r, magnitude };
}

// Draw the field
const gridSpacing = 90; // Grid spacing for arrows
for (let x = 0; x < width; x += gridSpacing) {
    for (let y = 0; y < height; y += gridSpacing) {
        const { fx, fy, magnitude } = calculateField(charge.q, charge.x, charge.y, x, y);

        // Scale the vector based on the reference field
        const scale = (fixedArrowLength * magnitude) / referenceFieldMagnitude;
        // const nx = fixedArrowLength * magnitude / referenceFieldMagnitude;
        // const ny = fixedArrowLength * magnitude / referenceFieldMagnitude;
        const nx = fx / magnitude * scale;
        const ny = fy / magnitude * scale;
        
        // Draw the arrow
        svg.append("line")
            .attr("class", "vector")
            .attr("x1", x)
            .attr("y1", y)
            .attr("x2", x + nx)
            .attr("y2", y + ny)
            .attr("stroke", "black")
            .attr("marker-end", "url(#arrow)");

        // Display the magnitude near the arrow
        svg.append("text")
            .attr("class", "field-value")
            .attr("x", x + nx * 0.5) // Place the text at the midpoint of the arrow
            .attr("y", y + ny * 0.5)
            .attr("dy", "-5") // Offset vertically for better visibility
            .text(Math.sqrt(fx * fx + fy * fy).toFixed(2)); // Display field strength
    }
}

// Draw the charge
svg.append("circle")
    .attr("cx", charge.x)
    .attr("cy", charge.y)
    .attr("r", 10)
    .attr("fill", "red");
