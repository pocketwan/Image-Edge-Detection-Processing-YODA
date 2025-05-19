`timescale 1ns/1ps

module median_filter (
    input wire clk,
    input wire rst,
    input wire [7:0] pixel_in,
    output reg [7:0] pixel_out
);
    parameter WIDTH = 256;

    // Line buffers
    reg [7:0] line_buf0 [0:WIDTH-1];
    reg [7:0] line_buf1 [0:WIDTH-1];

    // Shift registers for current 3 rows
    reg [7:0] shift0 [0:2];
    reg [7:0] shift1 [0:2];
    reg [7:0] shift2 [0:2];

    // Counters
    reg [15:0] col_cnt;
    reg [15:0] row_cnt;
      reg [7:0] window [0:8];
            reg [7:0] tmp;
            integer j, k;

    integer i;

    always @(posedge clk) begin
        if (rst) begin
            col_cnt <= 0;
            row_cnt <= 0;
            pixel_out <= 0;

            for (i = 0; i < WIDTH; i = i + 1) begin
                line_buf0[i] <= 0;
                line_buf1[i] <= 0;
            end

            for (i = 0; i < 3; i = i + 1) begin
                shift0[i] <= 0;
                shift1[i] <= 0;
                shift2[i] <= 0;
            end
        end else begin
            // Declare local variables at the top of procedural block
          
            // Shift in new pixels into shift registers
            shift0[0] <= shift0[1];
            shift0[1] <= shift0[2];
            shift0[2] <= line_buf0[col_cnt];

            shift1[0] <= shift1[1];
            shift1[1] <= shift1[2];
            shift1[2] <= line_buf1[col_cnt];

            shift2[0] <= shift2[1];
            shift2[1] <= shift2[2];
            shift2[2] <= pixel_in;

            // Update line buffers
            line_buf0[col_cnt] <= line_buf1[col_cnt];
            line_buf1[col_cnt] <= pixel_in;

            // Only compute median when enough data is available
            if (row_cnt >= 2 && col_cnt >= 2) begin
                // Copy values to window
                window[0] = shift0[0]; window[1] = shift0[1]; window[2] = shift0[2];
                window[3] = shift1[0]; window[4] = shift1[1]; window[5] = shift1[2];
                window[6] = shift2[0]; window[7] = shift2[1]; window[8] = shift2[2];

                // Odd-even sort (sufficient for 9 elements)
                for (j = 0; j < 5; j = j + 1) begin
                    for (k = 0; k < 8; k = k + 2) begin
                        if (window[k] > window[k+1]) begin
                            tmp = window[k];
                            window[k] = window[k+1];
                            window[k+1] = tmp;
                        end
                    end
                    for (k = 1; k < 8; k = k + 2) begin
                        if (window[k] > window[k+1]) begin
                            tmp = window[k];
                            window[k] = window[k+1];
                            window[k+1] = tmp;
                        end
                    end
                end

                // Median is the middle value after sorting
                pixel_out <= window[4];
            end else begin
                pixel_out <= 0;
            end

            // Update column and row counters
            if (col_cnt == WIDTH - 1) begin
                col_cnt <= 0;
                row_cnt <= row_cnt + 1;
            end else begin
                col_cnt <= col_cnt + 1;
            end
        end
    end
endmodule
