\ Model machine_shop_branching_geq
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xac1ecdcb81a3eafc
Maximize
  100 x[p] + 150 x[l]
Subject To
 purchase: 8000 x[p] + 4000 x[l] <= 40000
 floor_space: 15 x[p] + 30 x[l] <= 200
 branching_geq: x[l] >= 6
Bounds
End
