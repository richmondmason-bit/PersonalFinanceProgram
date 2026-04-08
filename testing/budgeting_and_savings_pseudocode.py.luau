local VolumetricLighting = {}

-- Easy Config List - Change these values to customize the effect
VolumetricLighting.Config = {
	VerticalRender = 10000,
	HorizontalRender = 10000,
	BeamTransparency = 0.9,
	BeamCount = 64,                    -- Lower = better performance (try 32 for mobile)
	BeamDensity = 0.8,
	BrightnessColor = Color3.new(1, 1, 1),   -- Change this for different colors (sunlight tint, etc.)
}

local Camera = workspace.CurrentCamera

local function MakeNewLightingBeam(Parent, Depth, BeamCount, Config)
	local Attachment0 = Instance.new("Attachment")
	local Attachment1 = Instance.new("Attachment")
	local Beam = Instance.new("Beam")
	
	local Percentile = Depth / BeamCount
	
	Attachment0.CFrame = CFrame.new(0, Config.VerticalRender / 2, Depth * Config.BeamDensity * -1)
	Attachment0.Parent = Parent
	
	Attachment1.CFrame = CFrame.new(0, -Config.VerticalRender / 2, Depth * Config.BeamDensity * -1)
	Attachment1.Parent = Parent
	
	Beam.LightEmission = 1
	Beam.Color = ColorSequence.new(Config.BrightnessColor)
	Beam.Transparency = NumberSequence.new(Config.BeamTransparency + ((1 - Config.BeamTransparency) * Percentile))
	Beam.Width0 = Config.HorizontalRender
	Beam.Width1 = Config.HorizontalRender
	Beam.Attachment0 = Attachment0
	Beam.Attachment1 = Attachment1
	Beam.FaceCamera = true
	Beam.Parent = Parent
end

local baseAttachment

function VolumetricLighting:Init()
	-- Clean up old effect if it exists
	if baseAttachment then
		self:Destroy()
	end
	
	-- Create the main attachment and parent it to the camera
	baseAttachment = Instance.new("Attachment")
	baseAttachment.Parent = Camera
	
	local cfg = self.Config
	local count = cfg.BeamCount
	
	-- Create all the lighting beams
	for Depth = 1, count do
		MakeNewLightingBeam(baseAttachment, Depth, count, cfg)
	end
end

function VolumetricLighting:Destroy()
	if baseAttachment then
		baseAttachment:Destroy()
		baseAttachment = nil
	end
end

return VolumetricLighting