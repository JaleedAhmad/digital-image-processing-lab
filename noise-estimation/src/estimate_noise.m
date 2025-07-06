function noise_type = estimate_noise(noisy_image)
    % This function estimates the type of noise in an image, optimized for chess board images
    % by focusing on edge regions and local variations
    
    % Convert image to double if not already
    if ~isa(noisy_image, 'double')
        noisy_image = im2double(noisy_image);
    end
    
    % Get edge regions using Sobel
    [Gx, Gy] = imgradientxy(noisy_image);
    edge_mag = sqrt(Gx.^2 + Gy.^2);
    edge_mask = edge_mag > 0.1;
    
    % Analyze noise in non-edge regions
    non_edge_mask = ~edge_mask;
    non_edge_pixels = noisy_image(non_edge_mask);
    
    if isempty(non_edge_pixels)
        noise_type = 'unknown';
        return;
    end
    
    % Calculate statistics for non-edge regions
    local_var = stdfilt(noisy_image).^2;
    mean_local_var = mean(local_var(non_edge_mask));
    
    % Calculate noise characteristics
    [counts, edges] = histcounts(non_edge_pixels, 'BinMethod', 'scott');
    bin_centers = (edges(1:end-1) + edges(2:end))/2;
    
    % Normalize histogram
    counts = counts / sum(counts);
    
    % Calculate statistical measures
    noise_skewness = skewness(non_edge_pixels);
    noise_kurtosis = kurtosis(non_edge_pixels);
    noise_range = range(non_edge_pixels);
    
    % Check for impulse noise (Salt & Pepper)
    extreme_ratio = sum(non_edge_pixels < 0.1 | non_edge_pixels > 0.9) / length(non_edge_pixels);
    
    % Calculate local variation metric
    local_diff = abs(diff(non_edge_pixels));
    variation_metric = mean(local_diff);
    
    % Debug information
    fprintf('Debug Info for Noise Estimation:\n');
    fprintf('Mean local variance: %.4f\n', mean_local_var);
    fprintf('Noise skewness: %.4f\n', noise_skewness);
    fprintf('Noise kurtosis: %.4f\n', noise_kurtosis);
    fprintf('Noise range: %.4f\n', noise_range);
    fprintf('Extreme ratio: %.4f\n', extreme_ratio);
    fprintf('Variation metric: %.4f\n', variation_metric);
    
    % Decision logic based on noise characteristics
    if extreme_ratio > 0.1 && variation_metric > 0.2
        noise_type = 'salt & pepper';
    elseif abs(noise_skewness) < 0.3 && abs(noise_kurtosis - 3) < 1 && mean_local_var < 0.1
        noise_type = 'gaussian';
    elseif abs(noise_skewness) < 0.2 && abs(noise_kurtosis - 1.8) < 0.5 && noise_range < 0.5
        noise_type = 'uniform';
    elseif noise_skewness > 0.5 && noise_skewness < 2 && mean_local_var > 0.05
        noise_type = 'rayleigh';
    elseif noise_skewness > 1 && noise_kurtosis > 4
        noise_type = 'exponential';
    else
        noise_type = 'unknown';
    end
    
    fprintf('Estimated noise type: %s\n\n', noise_type);
end

