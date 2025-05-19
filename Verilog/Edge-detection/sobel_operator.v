module sobel_filter(
    input  wire [7:0] P00, P01, P02,
    input  wire [7:0] P10, P11, P12,
    input  wire [7:0] P20, P21, P22,
    output wire [7:0] edge_mag
);

    wire signed [10:0] Gx, Gy;
    wire signed [10:0] abs_Gx, abs_Gy;
    wire signed [10:0] mag;

    // Compute Gx
    assign Gx = -$signed({3'b000, P00}) - (2 * $signed({3'b000, P10})) - $signed({3'b000, P20}) +
                 $signed({3'b000, P02}) + (2 * $signed({3'b000, P12})) + $signed({3'b000, P22});

    // Compute Gy
    assign Gy = -$signed({3'b000, P00}) - (2 * $signed({3'b000, P01})) - $signed({3'b000, P02}) +
                 $signed({3'b000, P20}) + (2 * $signed({3'b000, P21})) + $signed({3'b000, P22});

    // Absolute values
    assign abs_Gx = (Gx < 0) ? -Gx : Gx;
    assign abs_Gy = (Gy < 0) ? -Gy : Gy;

    // Sum magnitudes
    assign mag = abs_Gx + abs_Gy;

    // Clamp result to 255
    assign edge_mag = (mag > 255) ? 8'd255 : mag[7:0];

endmodule
