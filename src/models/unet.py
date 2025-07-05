import torch
import torch.nn as nn
import torch.nn.functional as F

class DoubleConv(nn.Module):
    """(convolution => [BN] => ReLU) * 2"""

    def __init__(self, in_channels, out_channels, mid_channels=None):
        super().__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.double_conv(x)

class Down(nn.Module):
    """Downscaling with maxpool then double conv"""

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)

class Up(nn.Module):
    """Upscaling then double conv"""

    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()

        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)
        else:
            self.up = nn.ConvTranspose2d(in_channels , in_channels // 2, kernel_size=2, stride=2)
            self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        # input is CHW
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]

        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)

class OutConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        return self.conv(x)

class UNet(nn.Module):
    """
    A standard UNet model for semantic segmentation.
    This architecture is designed to take our fused 3-channel input
    (OHRC, DTM, Slope) and output a segmentation map.
    """
    def __init__(self, n_channels, n_classes, bilinear=True):
        """
        Args:
            n_channels (int): Number of input channels (3 for our case).
            n_classes (int): Number of output classes (e.g., 3 for background, landslide, boulder).
            bilinear (bool): Whether to use bilinear upsampling or a transposed convolution.
        """
        super(UNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.bilinear = bilinear

        self.inc = DoubleConv(n_channels, 64)
        self.down1 = Down(64, 128)
        self.down2 = Down(128, 256)
        self.down3 = Down(256, 512)
        factor = 2 if bilinear else 1
        self.down4 = Down(512, 1024 // factor)
        self.up1 = Up(1024, 512 // factor, bilinear)
        self.up2 = Up(512, 256 // factor, bilinear)
        self.up3 = Up(256, 128 // factor, bilinear)
        self.up4 = Up(128, 64, bilinear)
        self.outc = OutConv(64, n_classes)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        logits = self.outc(x)
        return logits

if __name__ == '__main__':
    # This block demonstrates how to instantiate and use the UNet model.
    print("Running UNet model demonstration...")

    # --- Parameters for our Lunar Project ---
    # Input channels: 1 for OHRC, 1 for DTM, 1 for Slope
    input_channels = 3
    # Output classes: Background, Landslide, Boulder
    output_classes = 3

    # Create a model instance
    model = UNet(n_channels=input_channels, n_classes=output_classes)
    
    # Create a dummy input tensor that mimics our fused data
    # Batch size = 1, Channels = 3, Height = 256, Width = 256
    dummy_input = torch.randn(1, input_channels, 256, 256)

    print(f"Model instantiated: UNet with {input_channels} in_channels and {output_classes} out_classes.")
    print(f"Dummy input tensor shape: {dummy_input.shape}")

    # Perform a forward pass
    with torch.no_grad():
        output = model(dummy_input)

    print(f"Output tensor shape: {output.shape}")
    # Expected output shape: (Batch size, Num classes, Height, Width)
    # torch.Size([1, 3, 256, 256])

    # Check that the number of output channels matches the number of classes
    assert output.shape[1] == output_classes
    
    print("UNet model demonstration finished successfully.")


