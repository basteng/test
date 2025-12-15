#!/usr/bin/env python3

# 验证Total Return计算
previous_month_final_return = 316
call_price = 0.0095
put_price = 0.0046
call_contracts = 5
put_contracts = 11
remainder_cost = 40

current_option_value = int((call_contracts * call_price * 10000) + (put_contracts * put_price * 10000))
print(f"当前期权价值: {current_option_value}")

if previous_month_final_return > 0:
    total_return = int(previous_month_final_return + current_option_value + remainder_cost)
    print(f"Total Return应该是: {total_return}")
else:
    total_return = current_option_value + remainder_cost
    print(f"单月Total Return: {total_return}")

print(f"上月收益316 + 期权价值{current_option_value} + 余数{remainder_cost} = {316 + current_option_value + remainder_cost}")