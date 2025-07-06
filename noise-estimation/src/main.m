% Test script
test_noise_types = {'sp', 'gaussian', 'uniform', 'rayleigh', 'exp'};
img_num = 1;  % Test with first image

fprintf('Testing noise estimation for image %d:\n', img_num);
for i = 1:length(test_noise_types)
    img_path = sprintf('noisy_images/img%d_%s.png', img_num, test_noise_types{i});
    if exist(img_path, 'file')
        noisy_img = imread(img_path);
        fprintf('\nTesting %s noise:\n', test_noise_types{i});
        noise_type = estimate_noise(noisy_img);
    end
end