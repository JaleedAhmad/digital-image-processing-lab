% Noise Generation Script - Updated with more distinct noise patterns
% This script reads chess board images and adds different types of noise

% Create output directory if it doesn't exist
if ~exist('noisy_images', 'dir')
    mkdir('noisy_images');
end

% Parameters for noise - adjusted for better visibility
salt_pepper_density = 0.1;    % Increased density
gaussian_variance = 0.04;     % Increased variance
uniform_range = [-0.3 0.3];   % Increased range
rayleigh_scale = 0.2;        % Increased scale
exp_mean = 0.15;             % Increased mean

% Loop through all images
for img_num = 1:6
    % Read image
    if img_num == 2
        [img, cmap] = imread(sprintf('%d.png', img_num));
        img = ind2rgb(img, cmap);
    else
        img = imread(sprintf('%d.png', img_num));
    end
    
    % Convert to grayscale if RGB
    if size(img, 3) == 3
        img_gray = rgb2gray(img);
    else
        img_gray = img;
    end
    
    % Convert to double
    img_double = im2double(img_gray);
    
    % 1. Salt & Pepper Noise - More distinct
    noisy_sp = imnoise(img_double, 'salt & pepper', salt_pepper_density);
    imwrite(noisy_sp, sprintf('noisy_images/img%d_sp.png', img_num));
    
    % 2. Gaussian Noise - More spread out
    gaussian_noise = gaussian_variance * randn(size(img_double));
    noisy_gaussian = img_double + gaussian_noise;
    noisy_gaussian = max(0, min(1, noisy_gaussian));
    imwrite(noisy_gaussian, sprintf('noisy_images/img%d_gaussian.png', img_num));
    
    % 3. Uniform Noise - More noticeable
    uniform_noise = uniform_range(1) + (uniform_range(2)-uniform_range(1)).*rand(size(img_double));
    noisy_uniform = img_double + uniform_noise;
    noisy_uniform = max(0, min(1, noisy_uniform));
    imwrite(noisy_uniform, sprintf('noisy_images/img%d_uniform.png', img_num));
    
    % 4. Rayleigh Noise - More pronounced
    rayleigh_noise = rayleigh_scale * sqrt(-2 * log(1 - rand(size(img_double))));
    noisy_rayleigh = img_double + rayleigh_noise;
    noisy_rayleigh = max(0, min(1, noisy_rayleigh));
    imwrite(noisy_rayleigh, sprintf('noisy_images/img%d_rayleigh.png', img_num));
    
    % 5. Exponential Noise - More visible
    exp_noise = exprnd(exp_mean, size(img_double));
    noisy_exp = img_double + exp_noise;
    noisy_exp = max(0, min(1, noisy_exp));
    imwrite(noisy_exp, sprintf('noisy_images/img%d_exp.png', img_num));
end

disp('Noise generation completed with enhanced noise patterns!');