from torch.utils.data import DataLoader

   dataloader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=4, pin_memory=True)

# ===== cell separator =====

dataloader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=4, pin_memory=True, prefetch_factor=2)

# ===== cell separator =====

from torch.utils.data.distributed import DistributedSampler

   sampler = DistributedSampler(dataset)
   dataloader = DataLoader(dataset, batch_size=64, sampler=sampler, num_workers=4, pin_memory=True)

# ===== cell separator =====

def custom_collate_fn(batch):
       # Custom collation logic
       return collated_batch

   dataloader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=4, pin_memory=True, collate_fn=custom_collate_fn)

# ===== cell separator =====

subset = torch.utils.data.Subset(dataset, indices)
   dataloader = DataLoader(subset, batch_size=64, shuffle=True, num_workers=4, pin_memory=True)