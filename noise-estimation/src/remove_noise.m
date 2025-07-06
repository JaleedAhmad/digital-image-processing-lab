function denoised_img = remove_noise(noisy_image, noise_type)
    % This function removes noise based on the estimated noise type
    % Parameters:
    %   noisy_image: Input noisy image
    %   noise_type: String indicating the type of noise
    
    % Convert to double if not already
    if ~isa(noisy_image, 'double')
        noisy_image = im2double(noisy_image);
    end
    
    switch lower(noise_type)
        case 'salt & pepper'
            % Median filter works best for salt & pepper noise
            denoised_img = medfilt2(noisy_image, [3 3]);
            
        case 'gaussian'
            % Gaussian filter for Gaussian noise
            h = fspecial('gaussian', [5 5], 1);
            denoised_img = imfilter(noisy_image, h, 'replicate');
            
        case {'uniform', 'rayleigh', 'exponential'}
            % Wiener filter works well for these types of noise
            denoised_img = wiener2(noisy_image, [5 5]);
            
        otherwise
            % Default to median filtering if noise type is unknown
            denoised_img = medfilt2(noisy_image, [3 3]);
    end
end

% Main script to process all images
if ~exist('denoised_images', 'dir')
    mkdir('denoised_images');
end

noise_types = {'sp', 'gaussian', 'uniform', 'rayleigh', 'exp'};

% Process each image
for img_num = 1:6
    for i = 1:length(noise_types)
        % Read noisy image
        noisy_img = imread(sprintf('noisy_images/img%d_%s.png', img_num, noise_types{i}));
        
        % Estimate noise type
        estimated_noise = estimate_noise(noisy_img);
        
        % Remove noise
        denoised = remove_noise(noisy_img, estimated_noise);
        
        % Save result
        imwrite(denoised, sprintf('denoised_images/img%d_%s_denoised.png', img_num, noise_types{i}));
    end
end

disp('Noise removal completed successfully!');