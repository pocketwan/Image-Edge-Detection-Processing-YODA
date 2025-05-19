`timescale 1ns/1ps 

module tb_median_filter;

    parameter WIDTH = 256;
    parameter HEIGHT = 256;
    parameter TOTAL_PIXELS = WIDTH * HEIGHT;

    reg clk, rst;
    reg [7:0] pixel_in;
    wire [7:0] pixel_out;

    integer i, input_file, output_file, r;
    integer output_pixels;
    integer j;

    reg [7:0] image_mem [0:TOTAL_PIXELS-1];
    reg [7:0] output_mem [0:TOTAL_PIXELS-1];

    // Timing variables
    time start_time, end_time;
    integer cycle_count;  // Clock cycle counter

    // Instantiate the DUT
    median_filter dut (
        .clk(clk),
        .rst(rst),
        .pixel_in(pixel_in),
        .pixel_out(pixel_out)
    );

    // Clock generation
    initial clk = 0;
    always #5 clk = ~clk;

    // Load image from HEX file
    initial begin
        input_file = $fopen("C:/Users/USER/man_noisy.hex", "r");
        if (input_file == 0) begin
            $display("Failed to open input file");
            $finish;
        end

        for (i = 0; i < TOTAL_PIXELS; i = i + 1) begin
            r = $fscanf(input_file, "%h\n", image_mem[i]);
            if (r != 1) begin
                $display("Error reading pixel %0d", i);
                $finish;
            end
        end
        $fclose(input_file);
        $display("Image loaded successfully.");
    end

    // Apply reset
    initial begin
        rst = 1;
        pixel_in = 0;
        #20;
        rst = 0;
    end

    // Feed input pixels and collect output
    initial begin
  
        @(negedge rst);

        output_pixels = WIDTH * HEIGHT - 2*WIDTH - 2;  

        // Start timing and cycle count
        start_time = $time;
        cycle_count = 0;

        for (j = 0; j < WIDTH*HEIGHT; j = j + 1) begin
            pixel_in = image_mem[j];
            @(posedge clk);
            cycle_count = cycle_count + 1;

            if (j >= 2*WIDTH + 2) begin
                output_mem[j - (2*WIDTH + 2)] = pixel_out;
            end
        end

        // End timing
        end_time = $time;

        output_file = $fopen("C:/Users/USER/man_clean_hdl.hex", "w");
        if (output_file == 0) begin
            $display("Failed to open output file");
            $finish;
        end

        for (j = 0; j < output_pixels; j = j + 1) begin
            $fwrite(output_file, "%02h\n", output_mem[j]);
        end
        $fclose(output_file);

        $display("Done. Output has %0d pixels.", output_pixels);
        $display("Processing time: %0t ns", end_time - start_time);
        $display("Processing time: %0d clock cycles", cycle_count);

        $finish;
    end

endmodule
