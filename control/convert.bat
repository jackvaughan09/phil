set a = %~2
echo %a%
set b = %a:)=^)%
echo %b%
for %%G in (%1) do (%~2 %~3 %%G)