%% ANALYSE DE ROBUSTESSE DU STATE FEEDBACK
% TRANSFERT VERS UN AUTRE ROBOT

clear;
clc;
close all;

%% PARAMETRES NOMINAUX

p.g  = 9.81;

p.m  = 0.03;
p.R  = 0.042;

p.M  = 0.8;
p.W  = 0.152;
p.D  = 0.055;
p.H  = 0.160;
p.L  = p.H/2;

p.fm = 0.0022;
p.fw = 0;

p.Jm = 1e-5;
p.Rm = 6.69;
p.Kb = 0.468;
p.Kt = 0.317;
p.n  = 1;

%%  PARAMETRES A TESTER

parameters = {'m','R','M','L',...
              'fm','Jm','Rm','Kb','Kt','n'};

nParam = length(parameters);

%% VARIATIONS TESTEES

% Pas de 1 %
variations = -0.90:0.01:0.90;

nVar = length(variations);

%% GAIN STATE FEEDBACK

Kfb = [-0.2606 -18.0048 -0.7444 -1.75716];

%% MODELE NOMINAL

[A0,B0,~,~] = NXTway_model(p);

% Commande identique sur les deux moteurs
B0 = 2*B0(:,1);

%% POLES NOMINAUX

Acl0 = A0 - B0*Kfb;

poles_nominal = eig(Acl0);

%% IDENTIFICATION DU POLE DOMINANT NOMINAL

[~,idx_nominal] = max(real(poles_nominal));

lambda_dom_nominal = poles_nominal(idx_nominal);

%% GRANDEURS NOMINALES

% Temps caractéristique nominal
tau_nominal = ...
    1/abs(real(lambda_dom_nominal));

% Fréquence naturelle nominale
wn_nominal = abs(lambda_dom_nominal);

% Amortissement nominal
zeta_nominal = ...
    -real(lambda_dom_nominal)/abs(lambda_dom_nominal);

disp('============================================================');
disp('CARACTERISTIQUES NOMINALES');
disp('============================================================');

disp('Pôles nominaux :');
disp(poles_nominal);

fprintf('\n');

fprintf('Pole dominant : %f + %fi\n', ...
    real(lambda_dom_nominal), ...
    imag(lambda_dom_nominal));

fprintf('Temps caracteristique nominal : %.4f s\n', ...
    tau_nominal);

fprintf('Frequence naturelle nominale : %.4f rad/s\n', ...
    wn_nominal);

fprintf('Amortissement nominal : %.4f\n', ...
    zeta_nominal);

%% TOLERANCES DE PERFORMANCE

% Tolérance sur le temps caractéristique
tau_tolerance = 0.20;

% Tolérance sur l'amortissement
zeta_tolerance = 0.20;

%% MATRICES DE STOCKAGE

max_real_pole = zeros(nVar,nParam);

tau = nan(nVar,nParam);

zeta = nan(nVar,nParam);

wn = zeros(nVar,nParam);

stable = false(nVar,nParam);

acceptable_tau = false(nVar,nParam);

acceptable_zeta = false(nVar,nParam);

acceptable_performance = false(nVar,nParam);

%% ANALYSE PARAMETRE PAR PARAMETRE

for i = 1:nParam
    name = parameters{i};
    for j = 1:nVar
        variation = variations(j);
        %% Modification du paramètre

        p_test = p;

        p_test.(name) = ...
            p.(name)*(1 + variation);

        %% Nouveau modèle

        [A_test,B_test,~,~] = NXTway_model(p_test);

        B_test = 2*B_test(:,1);

        %%  Boucle fermée

        Acl_test = A_test - B_test*Kfb;

        %% Pôles

        poles_test = eig(Acl_test);

        %% Pôle dominant

        [max_real_pole(j,i),idx] = ...
            max(real(poles_test));

        lambda_dom = poles_test(idx);

        %% STABILITE

        stable(j,i) = max_real_pole(j,i) < 0;

        %% Temps caractéristique

        if stable(j,i)
            tau(j,i) = 1/abs(real(lambda_dom));
        end

        %% Fréquence naturelle

        wn(j,i) = abs(lambda_dom);

        %% Amortissement

        if abs(lambda_dom) > 0
            zeta(j,i) = -real(lambda_dom)/abs(lambda_dom);
        end

        %% CRITERE TEMPS CARACTERISTIQUE

        if stable(j,i)
            tau_min = tau_nominal*(1 - tau_tolerance);
            tau_max = tau_nominal*(1 + tau_tolerance);
            acceptable_tau(j,i) = ...
                tau(j,i) >= tau_min && ...
                tau(j,i) <= tau_max;
        end

        %% CRITERE AMORTISSEMENT

        if stable(j,i)
            zeta_min = zeta_nominal*(1 - zeta_tolerance);
            acceptable_zeta(j,i) = zeta(j,i) >= zeta_min;
        end

        %% PERFORMANCE GLOBALE

        acceptable_performance(j,i) = ...
            stable(j,i) && ...
            acceptable_tau(j,i) && ...
            acceptable_zeta(j,i);

    end
end

%% LIMITES DE STABILITE

stable_min = nan(nParam,1);
stable_max = nan(nParam,1);

%% LIMITES DE PERFORMANCE

performance_min = nan(nParam,1);
performance_max = nan(nParam,1);

for i = 1:nParam

    %% Stabilité

    idx = find(stable(:,i));
    if ~isempty(idx)
        stable_min(i) = variations(min(idx))*100;
        stable_max(i) = variations(max(idx))*100;
    end

    %% Performance

    idx = find(acceptable_performance(:,i));
    if ~isempty(idx)
        performance_min(i) = variations(min(idx))*100;
        performance_max(i) = variations(max(idx))*100;
    end

end

%% TOLERANCE SYMETRIQUE

% On prend la plus petite marge des deux côtés.

performance_tolerance = nan(nParam,1);
for i = 1:nParam
    if ~isnan(performance_min(i)) && ~isnan(performance_max(i))

        performance_tolerance(i) = ...
            min(abs(performance_min(i)), ...
                abs(performance_max(i)));
    end
end

%% CREATION DU TABLEAU FINAL

results = table( ...
    parameters', ...
    stable_min, ...
    stable_max, ...
    performance_min, ...
    performance_max, ...
    performance_tolerance, ...
    'VariableNames', ...
    {'Parameter',...
     'StableMin_percent',...
     'StableMax_percent',...
     'PerformanceMin_percent',...
     'PerformanceMax_percent',...
     'Tolerance_percent'} ...
);


%% CLASSEMENT

Class = cell(nParam,1);
for i = 1:nParam
    T = performance_tolerance(i);
    if isnan(T)
        Class{i} = 'CRITIQUE';
    elseif T < 10
        Class{i} = 'TRES CRITIQUE';
    elseif T < 20
        Class{i} = 'CRITIQUE';
    elseif T < 30
        Class{i} = 'IMPORTANTE';
    elseif T < 50
        Class{i} = 'FAIBLE';
    else
        Class{i} = 'NEGLIGEABLE';
    end
end

results.Class = Class;

%% TRI

results = sortrows( ...
    results, ...
    'Tolerance_percent');

%% AFFICHAGE

disp(' ');
disp('============================================================');
disp('ROBUSTESSE DU STATE FEEDBACK');
disp('============================================================');

disp(results);

%% GRAPHIQUES : STABILITE

for i = 1:nParam
    figure;
    plot(variations*100, ...
        max_real_pole(:,i), ...
        'o-', ...
        'LineWidth',1.2);
    hold on;
    yline(0,'--');
    xline(0,'--');
    grid on;
    xlabel('Variation du parametre [%]');
    ylabel('max(Re(\lambda))');
    title(['Stabilite - ',parameters{i}]);
end


%% GRAPHIQUES : TEMPS CARACTERISTIQUE

for i = 1:nParam
    figure;
    plot(variations*100, ...
        tau(:,i), ...
        'o-', ...
        'LineWidth',1.2);
    hold on;
    yline(tau_nominal*(1 + tau_tolerance),'--');
    yline(tau_nominal*(1 - tau_tolerance),'--');
    xline(0,'--');
    grid on;
    xlabel('Variation du parametre [%]');
    ylabel('\tau [s]');
    title(['Temps caracteristique - ',parameters{i}]);
end

%% GRAPHIQUES : AMORTISSEMENT

for i = 1:nParam
    figure;
    plot(variations*100, ...
        zeta(:,i), ...
        'o-', ...
        'LineWidth',1.2);
    hold on;
    yline(zeta_nominal*(1-zeta_tolerance),'--');
    xline(0,'--');
    grid on;
    xlabel('Variation du parametre [%]');
    ylabel('\zeta');
    title(['Amortissement - ',parameters{i}]);
end