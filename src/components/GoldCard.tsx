import React from 'react';
import { StyleSheet, View, ViewStyle, TouchableOpacity } from 'react-native';
import { Colors, Radius, Spacing, Shadow } from '../theme';

interface GoldCardProps {
  children: React.ReactNode;
  style?: ViewStyle;
  onPress?: () => void;
  elevated?: boolean;
  goldBorder?: boolean;
}

export function GoldCard({ children, style, onPress, elevated = false, goldBorder = false }: GoldCardProps) {
  const content = (
    <View
      style={[
        styles.card,
        elevated && styles.elevated,
        goldBorder && styles.goldBorder,
        style,
      ]}
    >
      {children}
    </View>
  );

  if (onPress) {
    return (
      <TouchableOpacity onPress={onPress} activeOpacity={0.82}>
        {content}
      </TouchableOpacity>
    );
  }

  return content;
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surface,
    borderRadius: Radius.md,
    padding: Spacing.md,
    ...Shadow.dark,
  },
  elevated: {
    backgroundColor: Colors.elevated,
    ...Shadow.gold,
  },
  goldBorder: {
    borderWidth: 1,
    borderColor: Colors.primary + '55', // 33% opacity
  },
});
