`timescale 1ns / 1ps

module sobel_top_tb;

  parameter WIDTH = 549;
  parameter HEIGHT = 319;
  parameter PIXELS = WIDTH * HEIGHT;

  reg [7:0] image_mem [0:PIXELS-1];
  reg [7:0] result_mem [0:PIXELS-1];
  reg [7:0] P[0:8];
  wire [7:0] edge_mag;

  sobel_filter sobel (
    .P00(P[0]), .P01(P[1]), .P02(P[2]),
    .P10(P[3]), .P11(P[4]), .P12(P[5]),
    .P20(P[6]), .P21(P[7]), .P22(P[8]),
    .edge_mag(edge_mag)
  );

  integer row, col, idx;

  initial begin
    $display("Start time: %0t",$time);
    $readmemh("input_cat_image_2.hex", image_mem);

    for (row = 1; row < HEIGHT - 1; row = row + 1) begin
      for (col = 1; col < WIDTH - 1; col = col + 1) begin
        P[0] = image_mem[(row-1)*WIDTH + (col-1)];
        P[1] = image_mem[(row-1)*WIDTH +  col   ];
        P[2] = image_mem[(row-1)*WIDTH + (col+1)];
        P[3] = image_mem[ row   *WIDTH + (col-1)];
        P[4] = image_mem[ row   *WIDTH +  col   ];
        P[5] = image_mem[ row   *WIDTH + (col+1)];
        P[6] = image_mem[(row+1)*WIDTH + (col-1)];
        P[7] = image_mem[(row+1)*WIDTH +  col   ];
        P[8] = image_mem[(row+1)*WIDTH + (col+1)];
        #1;
        idx = row * WIDTH + col;
        result_mem[idx] = edge_mag;
      end
    end

    $writememh("sobel_output_2.hex",result_mem);
    $display("Edge detection complete. Output written to sobel_output.hex");
    $display("Stop time: %0t",$time);
    $finish;
  end

endmodule
